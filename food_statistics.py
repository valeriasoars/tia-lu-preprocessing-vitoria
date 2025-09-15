class Statistics:
    """
    Uma classe para realizar cálculos estatísticos em um conjunto de dados.

    Atributos
    ----------
    dataset : dict[str, list]
        O conjunto de dados, estruturado como um dicionário onde as chaves
        são os nomes das colunas e os valores são listas com os dados.
    """
    def __init__(self, dataset):
        """
        Inicializa o objeto Statistics.

        Parâmetros
        ----------
        dataset : dict[str, list]
            O conjunto de dados, onde as chaves representam os nomes das
            colunas e os valores são as listas de dados correspondentes.
        """
        
        if not isinstance(dataset, dict):
            raise TypeError("O dataset deve ser um dicionário.")
        
        for value in dataset.values():
            if not isinstance(value, list):
               raise TypeError("Todos os valores no dicionário do dataset devem ser listas.") 
        
        if dataset:
            sizes = [len(value) for value in dataset.values()]
            if not all(size == sizes[0] for size in sizes):
                raise ValueError("Todas as colunas no dataset devem ter o mesmo tamanho.")
            
        self.dataset = dataset

    def _validate_column(self, column):
        if column not in self.dataset: 
            raise KeyError(f"A coluna '{column}' não existe no dataset")
    
    def _validate_numeric_column(self, column):
        self._validate_column(column)
        data = self.dataset[column]

        if data == []:
            return
        
        for value in data: 
            if not isinstance(value, (int, float)):
                raise TypeError(f"A coluna '{column}' deve ter apenas valores numéricos")
    
    def _deviation(self, column):

        deviation_list = []
        mean = self.mean(column)
        data = self.dataset[column]

        for value in data:
           deviation_list.append(value - mean)

        return deviation_list

    def mean(self, column):
        """
        Calcula a média aritmética de uma coluna.

        Fórmula:
        $$ \mu = \frac{1}{N} \sum_{i=1}^{N} x_i $$

        Parâmetros
        ----------
        column : str
            O nome da coluna (chave do dicionário do dataset).

        Retorno
        -------
        float
            A média dos valores na coluna.
        """
        self._validate_numeric_column(column)
        data = self.dataset[column]

        if data == []:
            return 0.0
        
        mean = sum(data) / len(data)
        return mean

    def median(self, column):
        """
        Calcula a mediana de uma coluna.

        A mediana é o valor central de um conjunto de dados ordenado.

        Parâmetros
        ----------
        column : str
            O nome da coluna (chave do dicionário do dataset).

        Retorno
        -------
        float
            O valor da mediana da coluna.
        """
        self._validate_numeric_column(column)
        data = self.dataset[column]
        sorted_data = sorted(data)

        size = len(sorted_data)

        if size < 1: return 0.0

        if size%2 == 0:
            return (sorted_data[size//2 - 1] + sorted_data[size//2]) / 2
        
        return sorted_data[size//2]

    def mode(self, column):
        """
        Encontra a moda (ou modas) de uma coluna.

        A moda é o valor que aparece com mais frequência no conjunto de dados.

        Parâmetros
        ----------
        column : str
            O nome da coluna (chave do dicionário do dataset).

        Retorno
        -------
        list
            Uma lista contendo o(s) valor(es) da moda.
        """
        self._validate_column(column)
        data = self.dataset[column]

        if data == []:
            return []
        
        mode = []
        frequencies = self.absolute_frequency(column)
        maxFrequency = max(frequencies.values())
        
        for item, frequency in frequencies.items():
            if frequency == maxFrequency: 
                mode.append(item)

        return mode

    def stdev(self, column):
        """
        Calcula o desvio padrão populacional de uma coluna.

        Fórmula:
        $$ \sigma = \sqrt{\frac{\sum_{i=1}^{N} (x_i - \mu)^2}{N}} $$

        Parâmetros
        ----------
        column : str
            O nome da coluna (chave do dicionário do dataset).

        Retorno
        -------
        float
            O desvio padrão dos valores na coluna.
        """
        self._validate_numeric_column(column)
        data = self.dataset[column]

        deviations = self._deviation(column)
        total_sum = 0.0

        if data == []: return 0.0

        for deviation in deviations:
            total_sum += deviation ** 2
        
        variance = total_sum/ len(data)
        stdev = variance ** 0.5
        
        return stdev

    def variance(self, column):
        """
        Calcula a variância populacional de uma coluna.

        Fórmula:
        $$ \sigma^2 = \frac{\sum_{i=1}^{N} (x_i - \mu)^2}{N} $$

        Parâmetros
        ----------
        column : str
            O nome da coluna (chave do dicionário do dataset).

        Retorno
        -------
        float
            A variância dos valores na coluna.
        """
        self._validate_numeric_column(column)
        data = self.dataset[column]

        if data == []:
            return 0.0
        
        mean_value = self.mean(column)
        
        squared_diffs = [(x - mean_value) ** 2 for x in data]
        variance = sum(squared_diffs) / len(data)
        return variance

    def covariance(self, column_a, column_b):
        """
        Calcula a covariância entre duas colunas.

        Fórmula:
        $$ \text{cov}(X, Y) = \frac{\sum_{i=1}^{N} (x_i - \mu_x)(y_i - \mu_y)}{N} $$

        Parâmetros
        ----------
        column_a : str
            O nome da primeira coluna (X).
        column_b : str
            O nome da segunda coluna (Y).

        Retorno
        -------
        float
            O valor da covariância entre as duas colunas.
        """
        deviationList = []

        self._validate_numeric_column(column_a)
        data_a = self.dataset[column_a]

        self._validate_numeric_column(column_b)
        data_b = self.dataset[column_b]

        if data_a == [] or data_b == []:
            return 0.0
        
        deviation_a = self._deviation(column_a)
        deviation_b = self._deviation(column_b)
        
        for i in range(len(data_a)):
            correspondentDeviation = deviation_a[i] * deviation_b[i]
            deviationList.append(correspondentDeviation)
        
        covariance = sum(deviationList) / len(data_a)
        return covariance


    def itemset(self, column):
        """
        Retorna o conjunto de itens únicos em uma coluna.

        Parâmetros
        ----------
        column : str
            O nome da coluna (chave do dicionário do dataset).

        Retorno
        -------
        set
            Um conjunto com os valores únicos da coluna.
        """
        self._validate_column(column)
        data = self.dataset[column]
        itemset = set(data)
        return itemset

    def absolute_frequency(self, column):
        """
        Calcula a frequência absoluta de cada item em uma coluna.

        Parâmetros
        ----------
        column : str
            O nome da coluna (chave do dicionário do dataset).

        Retorno
        -------
        dict
            Um dicionário onde as chaves são os itens e os valores são
            suas contagens (frequência absoluta).
        """
        self._validate_column(column)
        data = self.dataset[column]

        if data == []:
            return {}
        
        absolute_frequency = {}

        for value in data:
            if value not in absolute_frequency: 
                absolute_frequency[value] = 0

            absolute_frequency[value] += 1

        return absolute_frequency

    def relative_frequency(self, column):
        """
        Calcula a frequência relativa de cada item em uma coluna.

        Parâmetros
        ----------
        column : str
            O nome da coluna (chave do dicionário do dataset).

        Retorno
        -------
        dict
            Um dicionário onde as chaves são os itens e os valores são
            suas proporções (frequência relativa).
        """
        self._validate_column(column)
        data = self.dataset[column]

        if data == []:
            return {}
            
        absolute_frequencies = self.absolute_frequency(column)
        relative_frequency = {}

        
        total_frequencies = sum(absolute_frequencies.values())

        for value in absolute_frequencies:
            relative_frequency[value] = absolute_frequencies[value] / total_frequencies

        return relative_frequency 

    def cumulative_frequency(self, column, frequency_method='absolute'):
        """
        Calcula a frequência acumulada (absoluta ou relativa) de uma coluna.

        A frequência é calculada sobre os itens ordenados.

        Parâmetros
        ----------
        column : str
            O nome da coluna (chave do dicionário do dataset).
        frequency_method : str, opcional
            O método a ser usado: 'absolute' para contagem acumulada ou
            'relative' para proporção acumulada (padrão é 'absolute').

        Retorno
        -------
        dict
            Um dicionário ordenado com os itens como chaves e suas
            frequências acumuladas como valores.
        """
        absolute_frequency = self.absolute_frequency(column)
        absolute_cumulate_frequency = {}
        relative_cumulate_frequency = {}
        acumulator = 0

        self._validate_column(column)
        data = self.dataset[column]


        for value in sorted(absolute_frequency.keys()):
            acumulator += absolute_frequency[value]
            absolute_cumulate_frequency[value] = acumulator 
            relative_cumulate_frequency[value] = acumulator / len(data)
        
        if frequency_method == "absolute":
            return absolute_cumulate_frequency
        elif frequency_method == "relative":
            return relative_cumulate_frequency
        else:
            raise ValueError("O 'frequency_method' deve ser 'absolute' ou 'relative'.")

    def conditional_probability(self, column, value1, value2):
        """
        Calcula a probabilidade condicional P(X_i = value1 | X_{i-1} = value2).

        Este método trata a coluna como uma sequência e calcula a probabilidade
        de encontrar `value1` imediatamente após `value2`.

        Fórmula: P(A|B) = Contagem de sequências (B, A) / Contagem total de B

        Parâmetros
        ----------
        column : str
            O nome da coluna (chave do dicionário do dataset).
        value1 : any
            O valor do evento consequente (A).
        value2 : any
            O valor do evento condicionante (B).

        Retorno
        -------
        float
            A probabilidade condicional, um valor entre 0 e 1.
        """
        self._validate_column(column)
        data = self.dataset[column]

        if len(data) < 2:
            return 0.0
        
        count_value2 = data.count(value2)

        if count_value2 == 0:
            return 0.0 
        
        sequence_count = 0
        for i in range(len(data) - 1):
            if data[i] == value2 and data[i + 1] == value1:
                sequence_count += 1

        conditional_probability = sequence_count / count_value2
        return conditional_probability