"""
Módulo para análise estatística dos dados de partidas de LoL eSports.
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Union, Tuple
from functools import reduce


class StatsAnalyzer:
    """
    Classe responsável pela análise estatística dos dados.
    """
    
    def __init__(self, data: pd.DataFrame = None):
        """
        Inicializa o analisador estatístico.
        
        Args:
            data: DataFrame com os dados a serem analisados.
        """
        self.data = data
    
    def set_data(self, data: pd.DataFrame) -> None:
        """
        Define o DataFrame a ser analisado.
        
        Args:
            data: DataFrame com os dados.
        """
        self.data = data
    
    def get_basic_stats(self, columns: Optional[List[str]] = None) -> Dict:
        """
        Calcula estatísticas básicas para as colunas numéricas.
        
        Args:
            columns: Lista de colunas para calcular estatísticas. Se None, usa todas as colunas numéricas.
            
        Returns:
            Dicionário com estatísticas básicas.
        """
        if self.data is None:
            return {}
        
        # Se nenhuma coluna for especificada, usa todas as colunas numéricas
        if columns is None:
            numeric_data = self.data.select_dtypes(include=['float64', 'int64'])
        else:
            # Filtra apenas colunas numéricas da lista fornecida
            valid_columns = [col for col in columns if col in self.data.columns and 
                            pd.api.types.is_numeric_dtype(self.data[col])]
            numeric_data = self.data[valid_columns]
        
        # Usando funções de alta ordem para calcular estatísticas
        stats_functions = {
            'mean': np.mean,
            'median': np.median,
            'std': np.std,
            'min': np.min,
            'max': np.max,
            'count': len
        }
        
        # Calculando estatísticas para cada coluna
        stats = {}
        for col in numeric_data.columns:
            col_stats = {stat_name: stat_func(numeric_data[col].dropna()) 
                        for stat_name, stat_func in stats_functions.items()}
            stats[col] = col_stats
        
        return stats
    
    def get_correlation_matrix(self, columns: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Calcula a matriz de correlação entre as colunas numéricas.
        
        Args:
            columns: Lista de colunas para calcular correlações. Se None, usa todas as colunas numéricas.
            
        Returns:
            DataFrame com a matriz de correlação.
        """
        if self.data is None:
            return pd.DataFrame()
        
        # Se nenhuma coluna for especificada, usa todas as colunas numéricas
        if columns is None:
            numeric_data = self.data.select_dtypes(include=['float64', 'int64'])
        else:
            # Filtra apenas colunas numéricas da lista fornecida
            valid_columns = [col for col in columns if col in self.data.columns and 
                            pd.api.types.is_numeric_dtype(self.data[col])]
            numeric_data = self.data[valid_columns]
        
        # Calculando a matriz de correlação
        return numeric_data.corr()
    
    def get_categorical_distribution(self, column: str) -> Dict:
        """
        Calcula a distribuição de valores para uma coluna categórica.
        
        Args:
            column: Nome da coluna categórica.
            
        Returns:
            Dicionário com a contagem de cada valor.
        """
        if self.data is None or column not in self.data.columns:
            return {}
        
        # Verificando se a coluna é categórica
        if not pd.api.types.is_object_dtype(self.data[column]):
            return {}
        
        # Calculando a distribuição
        distribution = self.data[column].value_counts().to_dict()
        return distribution
    
    def get_time_series_analysis(self, date_column: str, value_column: str, 
                                freq: str = 'M') -> pd.DataFrame:
        """
        Realiza análise de série temporal para uma coluna de valor.
        
        Args:
            date_column: Nome da coluna de data.
            value_column: Nome da coluna de valor.
            freq: Frequência para agrupamento ('D' para diário, 'W' para semanal, 'M' para mensal).
            
        Returns:
            DataFrame com a série temporal.
        """
        if self.data is None or date_column not in self.data.columns or value_column not in self.data.columns:
            return pd.DataFrame()
        
        # Verificando se a coluna de data é do tipo datetime
        if not pd.api.types.is_datetime64_dtype(self.data[date_column]):
            try:
                # Tentando converter para datetime
                date_series = pd.to_datetime(self.data[date_column])
            except:
                return pd.DataFrame()
        else:
            date_series = self.data[date_column]
        
        # Criando um DataFrame temporário com as colunas necessárias
        temp_df = pd.DataFrame({
            'date': date_series,
            'value': self.data[value_column]
        })
        
        # Agrupando por data e calculando estatísticas
        time_series = temp_df.groupby(pd.Grouper(key='date', freq=freq)).agg({
            'value': ['mean', 'median', 'std', 'count']
        }).reset_index()
        
        # Achatando o MultiIndex das colunas
        time_series.columns = ['date', 'mean', 'median', 'std', 'count']
        
        return time_series
    
    def get_group_comparison(self, group_column: str, value_column: str) -> Dict:
        """
        Compara estatísticas de um valor entre diferentes grupos.
        
        Args:
            group_column: Nome da coluna de agrupamento.
            value_column: Nome da coluna de valor.
            
        Returns:
            Dicionário com estatísticas por grupo.
        """
        if self.data is None or group_column not in self.data.columns or value_column not in self.data.columns:
            return {}
        
        # Verificando se a coluna de valor é numérica
        if not pd.api.types.is_numeric_dtype(self.data[value_column]):
            return {}
        
        # Agrupando e calculando estatísticas
        grouped_stats = self.data.groupby(group_column)[value_column].agg([
            'mean', 'median', 'std', 'min', 'max', 'count'
        ]).to_dict(orient='index')
        
        return grouped_stats
    
    def get_top_n_records(self, column: str, n: int = 10, ascending: bool = False) -> pd.DataFrame:
        """
        Retorna os N melhores ou piores registros com base em uma coluna.
        
        Args:
            column: Nome da coluna para ordenação.
            n: Número de registros a retornar.
            ascending: Se True, retorna os menores valores; se False, os maiores.
            
        Returns:
            DataFrame com os N registros.
        """
        if self.data is None or column not in self.data.columns:
            return pd.DataFrame()
        
        # Ordenando e selecionando os N primeiros registros
        sorted_data = self.data.sort_values(by=column, ascending=ascending)
        return sorted_data.head(n)
    
    def calculate_win_rates(self, group_column: str) -> Dict:
        """
        Calcula taxas de vitória para diferentes grupos.
        
        Args:
            group_column: Nome da coluna de agrupamento (ex: 'champion', 'teamname').
            
        Returns:
            Dicionário com taxas de vitória por grupo.
        """
        if self.data is None or group_column not in self.data.columns or 'result' not in self.data.columns:
            return {}
        
        # Agrupando por coluna e calculando taxa de vitória
        win_rates = self.data.groupby(group_column)['result'].agg(
            games_played=('count'),
            wins=('sum'),  # Assumindo que 'result' é 1 para vitória e 0 para derrota
        ).reset_index()
        
        # Calculando taxa de vitória
        win_rates['win_rate'] = win_rates['wins'] / win_rates['games_played']
        
        # Convertendo para dicionário
        win_rates_dict = win_rates.set_index(group_column).to_dict(orient='index')
        
        return win_rates_dict
    
    def get_performance_metrics(self) -> Dict:
        """
        Calcula métricas de desempenho específicas para LoL.
        
        Returns:
            Dicionário com métricas de desempenho.
        """
        if self.data is None:
            return {}
        
        metrics = {}
        
        # Métricas relevantes para LoL
        if all(col in self.data.columns for col in ['kills', 'deaths', 'assists']):
            # Média de KDA
            metrics['avg_kda'] = self.data.apply(
                lambda row: (row['kills'] + row['assists']) / max(1, row['deaths']), 
                axis=1
            ).mean()
        
        if 'gamelength' in self.data.columns:
            # Duração média das partidas (em minutos)
            metrics['avg_game_duration'] = self.data['gamelength'].mean() / 60
        
        if 'firstblood' in self.data.columns:
            # Taxa de primeiro abate
            metrics['first_blood_rate'] = self.data['firstblood'].mean()
        
        # Adicionando mais métricas específicas de LoL
        for metric in ['dragons', 'barons', 'towers', 'inhibitors']:
            if metric in self.data.columns:
                metrics[f'avg_{metric}'] = self.data[metric].mean()
        
        return metrics
