import pandas as pd

class DataAnalyzer:
    """
    Classe para geração de análises estatísticas e visualização.
    """
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def get_basic_statistics(self) -> dict:
        """
        Retorna estatísticas básicas (média, mediana, desvio padrão) para colunas numéricas.
        """
        numeric_cols = self.df.select_dtypes(include='number').columns
        stats = {}
        for col in numeric_cols:
            stats[col] = {
                "mean": float(self.df[col].mean()),
                "median": float(self.df[col].median()),
                "std": float(self.df[col].std()),
            }
        return stats

    def get_record(self, record_id: int) -> dict:
        """
        Retorna informações de um registro específico com base em seu ID.
        """
        # Presume-se que exista uma coluna 'id' no DataFrame
        record = self.df[self.df['id'] == record_id]
        if record.empty:
            raise ValueError(f"Registro com id {record_id} não encontrado.")
        return record.to_dict(orient='records')[0]
