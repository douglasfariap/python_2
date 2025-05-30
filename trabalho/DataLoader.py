import pandas as pd

class DataLoader:
    """
    Classe para carregamento e pré-processamento dos dados.
    Posteriormente, implementar load_data e qualquer etapa de pré-processamento.
    """
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.df = None

    def load_data(self):
        # Carregar os dados (ex: CSV)
        self.df = pd.read_csv(self.data_path)
        # Aqui você pode adicionar etapas de pré-processamento
        # Ex: conversão de tipos, limpeza de valores nulos, etc.
        return self.df