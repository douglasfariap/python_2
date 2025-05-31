"""
Módulo para carregamento e pré-processamento dos dados de partidas de LoL eSports.
"""
import pandas as pd
from typing import Dict, List, Optional, Union, Callable
from functools import reduce
import numpy as np


class DataLoader:
    """
    Classe responsável pelo carregamento e pré-processamento dos dados.
    """
    
    def __init__(self, file_path: str):
        """
        Inicializa o carregador de dados.
        
        Args:
            file_path: Caminho para o arquivo CSV com os dados.
        """
        self.file_path = file_path
        self.data = None
        self.player_data = None
        self.team_data = None
    
    def load_data(self) -> pd.DataFrame:
        """
        Carrega os dados do arquivo CSV.
        
        Returns:
            DataFrame com os dados carregados.
        """
        # Usando low_memory=False para evitar o warning de tipos mistos
        self.data = pd.read_csv(self.file_path, low_memory=False)
        return self.data
    
    def preprocess_data(self) -> pd.DataFrame:
        """
        Realiza o pré-processamento dos dados.
        
        Returns:
            DataFrame com os dados pré-processados.
        """
        if self.data is None:
            self.load_data()
        
        # Aplicando funções de alta ordem para limpeza de dados
        cleaning_pipeline = [
            self._handle_missing_values,
            self._convert_data_types,
            self._add_derived_features
        ]
        
        # Usando reduce (paradigma funcional) para aplicar sequencialmente as funções
        self.data = reduce(lambda df, func: func(df), cleaning_pipeline, self.data)
        
        # Separando dados de jogadores e times
        self._split_data()
        
        return self.data
    
    def _handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Trata valores ausentes no DataFrame.
        
        Args:
            df: DataFrame a ser processado.
            
        Returns:
            DataFrame com valores ausentes tratados.
        """
        # Substituindo valores NaN em colunas numéricas por 0
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
        df[numeric_cols] = df[numeric_cols].fillna(0)
        
        # Substituindo valores NaN em colunas categóricas por 'unknown'
        categorical_cols = df.select_dtypes(include=['object']).columns
        df[categorical_cols] = df[categorical_cols].fillna('unknown')
        
        return df
    
    def _convert_data_types(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Converte tipos de dados para formatos apropriados.
        
        Args:
            df: DataFrame a ser processado.
            
        Returns:
            DataFrame com tipos de dados convertidos.
        """
        # Convertendo colunas de data
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
        
        # Convertendo colunas booleanas
        bool_cols = ['playoffs', 'firstblood', 'firstbloodkill', 'firstbloodassist', 'firstbloodvictim']
        for col in bool_cols:
            if col in df.columns:
                df[col] = df[col].astype(bool)
        
        return df
    
    def _add_derived_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Adiciona features derivadas que podem ser úteis para análise.
        
        Args:
            df: DataFrame a ser processado.
            
        Returns:
            DataFrame com features adicionais.
        """
        # Calculando KDA (Kills + Assists) / Deaths
        if all(col in df.columns for col in ['kills', 'deaths', 'assists']):
            # Usando expressão lambda (paradigma funcional)
            df['kda'] = df.apply(
                lambda row: (row['kills'] + row['assists']) / max(1, row['deaths']), 
                axis=1
            )
        
        # Calculando taxa de participação em abates
        if all(col in df.columns for col in ['kills', 'assists', 'teamkills']):
            df['kill_participation'] = df.apply(
                lambda row: (row['kills'] + row['assists']) / max(1, row['teamkills']) 
                if row['teamkills'] > 0 else 0,
                axis=1
            )
        
        return df
    
    def _split_data(self) -> None:
        """
        Separa os dados em dados de jogadores e dados de times.
        """
        if self.data is None:
            return
        
        # Filtrando dados de jogadores (com nome de jogador)
        self.player_data = self.data[self.data['playername'].notna()]
        
        # Filtrando dados de times (sem nome de jogador, mas com nome de time)
        self.team_data = self.data[
            (self.data['playername'].isna()) & 
            (self.data['teamname'].notna())
        ]
    
    def filter_data(self, filters: Dict) -> pd.DataFrame:
        """
        Filtra os dados com base em critérios específicos.
        
        Args:
            filters: Dicionário com os critérios de filtragem.
            
        Returns:
            DataFrame filtrado.
        """
        if self.data is None:
            self.preprocess_data()
        
        filtered_data = self.data.copy()
        
        # Aplicando cada filtro usando filter (paradigma funcional)
        for column, value in filters.items():
            if column in filtered_data.columns:
                if isinstance(value, list):
                    filtered_data = filtered_data[filtered_data[column].isin(value)]
                else:
                    filtered_data = filtered_data[filtered_data[column] == value]
        
        return filtered_data
    
    def get_unique_values(self, column: str) -> List:
        """
        Retorna valores únicos de uma coluna.
        
        Args:
            column: Nome da coluna.
            
        Returns:
            Lista de valores únicos.
        """
        if self.data is None:
            self.preprocess_data()
        
        if column in self.data.columns:
            return self.data[column].unique().tolist()
        return []
    
    def get_record_by_id(self, record_id: str) -> Optional[Dict]:
        """
        Retorna um registro específico pelo ID.
        
        Args:
            record_id: ID do registro a ser buscado.
            
        Returns:
            Dicionário com os dados do registro ou None se não encontrado.
        """
        if self.data is None:
            self.preprocess_data()
        
        # Buscando pelo ID (assumindo que gameid é o identificador)
        record = self.data[self.data['gameid'] == record_id]
        
        if record.empty:
            return None
        
        # Convertendo para dicionário e retornando o primeiro registro
        return record.iloc[0].to_dict()
    
    def apply_function_to_column(self, column: str, func: Callable) -> pd.Series:
        """
        Aplica uma função a uma coluna específica.
        
        Args:
            column: Nome da coluna.
            func: Função a ser aplicada.
            
        Returns:
            Série com os resultados da aplicação da função.
        """
        if self.data is None:
            self.preprocess_data()
        
        if column in self.data.columns:
            # Aplicando a função (paradigma funcional)
            return self.data[column].apply(func)
        
        return pd.Series()
