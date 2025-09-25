from food_statistics import Statistics
from typing import Dict, List, Set, Any

class MissingValueProcessor:
    """
    Processa valores ausentes (representados como None) no dataset.
    """
    def __init__(self, dataset: Dict[str, List[Any]]):
        self.dataset = dataset
        self.stats = Statistics(dataset)

    def _get_target_columns(self, columns: Set[str]) -> List[str]:
        """Retorna as colunas a serem processadas. Se 'columns' for vazio, retorna todas as colunas."""
        return list(columns) if columns else list(self.dataset.keys())
    
    def isna(self, columns: Set[str] = None) -> Dict[str, List[Any]]:
        """
        Retorna um novo dataset contendo apenas as linhas que possuem
        pelo menos um valor nulo (None) em uma das colunas especificadas.

        Args:
            columns (Set[str]): Um conjunto de nomes de colunas a serem verificadas.
                               Se vazio, todas as colunas são consideradas.
        Returns:
            Dict[str, List[Any]]: Um dicionário representando as linhas com valores nulos.
        """
        data = self.dataset
        target_columns = self._get_target_columns(columns)
        lines_length = len(data[target_columns[0]]) #verificar se todas as linhas tem o mesmo tamanho? 
        empty_value_data = {col: [] for col in target_columns}
        
        for idx_line in range(lines_length):
            if any(data[col][idx_line] is None for col in target_columns):
                for col in target_columns:
                    empty_value_data[col].append(data[col][idx_line])

        return empty_value_data

    def notna(self, columns: Set[str] = None) -> Dict[str, List[Any]]:
        """
        Retorna um novo dataset contendo apenas as linhas que não possuem
        valores nulos (None) em nenhuma das colunas especificadas.

        Args:
            columns (Set[str]): Um conjunto de nomes de colunas a serem verificadas.
                               Se vazio, todas as colunas são consideradas.

        Returns:
            Dict[str, List[Any]]: Um dicionário representando as linhas sem valores nulos.
        """
        data = self.dataset

        target_columns = self._get_target_columns(columns)
        lines_length = len(data[target_columns[0]])

        not_empty_value_data = {col: [] for col in target_columns}
        
        for idx_line in range(lines_length):
            if all(data[col][idx_line] is not None for col in target_columns):
                for col in target_columns:
                    not_empty_value_data[col].append(data[col][idx_line])

        return not_empty_value_data

    def fillna(self, columns: Set[str] = None, method: str = 'mean', default_value: Any = 0):
        """
        Preenche valores nulos (None) nas colunas especificadas usando um método.
        Modifica o dataset da classe.

        Args:
            columns (Set[str]): Colunas onde o preenchimento será aplicado. Se vazio, aplica a todas.
            method (str): 'mean', 'median', 'mode', ou 'default_value'.
            default_value (Any): Valor para usar com o método 'default_value'.
        """
        data = self.dataset

        target_columns = self._get_target_columns(columns)
        
        for col in target_columns:
            fill_value = 0
            if method == 'mean':
                    fill_value = self.stats.mean(col)
            elif method == 'median':
                    fill_value = self.stats.median(col)
            elif method == 'mode':
                if self.stats.mode(col):
                    fill_value = self.stats.mode(col)[0]
                else: fill_value = default_value
            elif method == 'default_value':
                fill_value = default_value

            for line, value in enumerate(data[col]):
                if value is None:
                    data[col][line] = fill_value
                
                    
                    

    def dropna(self, columns: Set[str] = None):
        """
        Remove as linhas que contêm valores nulos (None) nas colunas especificadas.
        Modifica o dataset da classe.

        Args:
            columns (Set[str]): Colunas a serem verificadas para valores nulos. Se vazio, todas as colunas são verificadas.
        """
        data = self.dataset

        target_columns = self._get_target_columns(columns)
        lines_length = len(data[target_columns[0]])

        idx_to_delete = []
        
        for idx_line in range(lines_length):
            if any(data[col][idx_line] is None for col in target_columns):
                idx_to_delete.append(idx_line)
        
        reversed_idx_del_list = sorted(idx_to_delete, reverse=True)

        for idx in reversed_idx_del_list:
            for col in data:
                del data[col][idx] # remoção direta pelos índices originais? 
class Scaler:
    """
    Aplica transformações de escala em colunas numéricas do dataset.
    """
    def __init__(self, dataset: Dict[str, List[Any]]):
        self.dataset = dataset
        self.stats = Statistics(dataset)

    def _get_target_columns(self, columns: Set[str]) -> List[str]:
        return list(columns) if columns else list(self.dataset.keys())

    def minMax_scaler(self, columns: Set[str] = None):
        """
        Aplica a normalização Min-Max ($X_{norm} = \frac{X - X_{min}}{X_{max} - X_{min}}$)
        nas colunas especificadas. Modifica o dataset.

        Args:
            columns (Set[str]): Colunas para aplicar o scaler. Se vazio, tenta aplicar a todas.
        """
        target_columns = self._get_target_columns(columns)

        for col in target_columns:
            self.stats._validate_numeric_column(col)
            data = self.dataset[col]
 
            valid_values = [x for x in data if x is not None]
            if valid_values:
                min_value = min(valid_values)
                max_value = max(valid_values)
                
                if max_value == min_value:
                    self.dataset[col] = [0.0 if x is not None else None for x in data]
                else:
                    self.dataset[col] = [(x - min_value) / (max_value - min_value) if x is not None else None for x in data]

    def standard_scaler(self, columns: Set[str] = None):
        """
        Aplica a padronização Z-score ($X_{std} = \frac{X - \mu}{\sigma}$)
        nas colunas especificadas. Modifica o dataset.

        Args:
            columns (Set[str]): Colunas para aplicar o scaler. Se vazio, tenta aplicar a todas.
        """
        target_columns = self._get_target_columns(columns)
        for col in target_columns:
            self.stats._validate_numeric_column(col)
            data = self.dataset[col]
            
            if data: 
                mean_val = self.stats.mean(col)
                std_val = self.stats.stdev(col)
                
            self.dataset[col] = [
                0.0 if x is not None and std_val == 0 else
                (x - mean_val) / std_val if x is not None else None
                for x in data
            ]
class Encoder:
    """
    Aplica codificação em colunas categóricas.
    """
    def __init__(self, dataset: Dict[str, List[Any]]):
        self.dataset = dataset

    def label_encode(self, columns: Set[str]):
        """
        Converte cada categoria em uma coluna em um número inteiro.
        Modifica o dataset.

        Args:
            columns (Set[str]): Colunas categóricas para codificar.
        """

        for col in columns:
            values = [v if v is not None else '__MISSING__' for v in self.dataset[col]]
            unique_categories_sorted = sorted(set(values))

            list_map = {item: i for i, item in enumerate(unique_categories_sorted)}
            encoded_values = [list_map[value] for value in values]
            
            self.dataset[col] = encoded_values


    def oneHot_encode(self, columns: Set[str]):
        """
        Cria novas colunas binárias para cada categoria nas colunas especificadas (One-Hot Encoding).
        Modifica o dataset adicionando e removendo colunas.

        Args:
            columns (Set[str]): Colunas categóricas para codificar.
        """
        for col in columns:
            values = [v if v is not None else '__MISSING__' for v in self.dataset[col]]
            unique_categories_sorted = sorted(set(values))

            for cat in unique_categories_sorted:
                new_col = f"{col}_{cat}"
                self.dataset[new_col] = [1 if value == cat else 0 for value in values]

            del self.dataset[col]
class Preprocessing:
    """
    Classe principal que orquestra as operações de pré-processamento de dados.
    """
    def __init__(self, dataset: Dict[str, List[Any]]):
        self.dataset = dataset
        self._validate_dataset_shape()
        
        # Atributos compostos para cada tipo de tarefa
        self.statistics = Statistics(self.dataset)
        self.missing_values = MissingValueProcessor(self.dataset)
        self.scaler = Scaler(self.dataset)
        self.encoder = Encoder(self.dataset)

    def _validate_dataset_shape(self):
        """
        Valida se todas as listas (colunas) no dicionário do dataset
        têm o mesmo comprimento.
        """
        sizes = [len(col) for col in self.dataset.values()]
        if not all(size == sizes[0] for size in sizes):
            raise ValueError("Todas as colunas no dataset devem ter o mesmo tamanho.")

    def isna(self, columns: Set[str] = None) -> Dict[str, List[Any]]:
        """
        Atalho para missing_values.isna(). Retorna as linhas com valores nulos.
        """
        return self.missing_values.isna(columns=columns)

    def notna(self, columns: Set[str] = None) -> Dict[str, List[Any]]:
        """
        Atalho para missing_values.notna(). Retorna as linhas sem valores nulos.
        """
        return self.missing_values.notna(columns=columns)

    def fillna(self, columns: Set[str] = None, method: str = 'mean', default_value: Any = 0):
        """
        Atalho para missing_values.fillna(). Preenche valores nulos.
        Retorna 'self' para permitir encadeamento de métodos.
        """
        self.missing_values.fillna(columns=columns, method=method, default_value=default_value)
        return self

    def dropna(self, columns: Set[str] = None):
        """
        Atalho para missing_values.dropna(). Remove linhas com valores nulos.
        Retorna 'self' para permitir encadeamento de métodos.
        """
        self.missing_values.dropna(columns=columns)
        return self

    def scale(self, columns: Set[str] = None, method: str = 'minMax'):
        """
        Aplica escalonamento nas colunas especificadas.

        Args:
            columns (Set[str]): Colunas para aplicar o escalonamento.
            method (str): O método a ser usado: 'minMax' ou 'standard'.

        Retorna 'self' para permitir encadeamento de métodos.
        """
        if method == 'minMax':
            self.scaler.minMax_scaler(columns=columns)
        elif method == 'standard':
            self.scaler.standard_scaler(columns=columns)
        else:
            raise ValueError(f"Método de escalonamento '{method}' não suportado. Use 'minMax' ou 'standard'.")
        return self

    def encode(self, columns: Set[str], method: str = 'label'):
        """
        Aplica codificação nas colunas especificadas.

        Args:
            columns (Set[str]): Colunas para aplicar a codificação.
            method (str): O método a ser usado: 'label' ou 'oneHot'.
        
        Retorna 'self' para permitir encadeamento de métodos.
        """
        if not columns:
            print("Aviso: Nenhuma coluna especificada para codificação. Nenhuma ação foi tomada.")
            return self

        if method == 'label':
            self.encoder.label_encode(columns=columns)
        elif method == 'oneHot':
            self.encoder.oneHot_encode(columns=columns)
        else:
            raise ValueError(f"Método de codificação '{method}' não suportado. Use 'label' ou 'oneHot'.")
        return self








