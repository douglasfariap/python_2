"""
Rotas para estatísticas da API.
"""
from flask import Blueprint, jsonify
import pandas as pd
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from models.data_loader import DataLoader
from models.stats_analyzer import StatsAnalyzer

# Criando o blueprint
stats_bp = Blueprint('statistics', __name__)

# Caminho para o dataset
DATA_PATH = '/home/ubuntu/upload/2022_LoL_esports_match_data_from_OraclesElixir.csv'

# Instanciando o carregador de dados e o analisador estatístico
data_loader = DataLoader(DATA_PATH)
stats_analyzer = StatsAnalyzer()

@stats_bp.route('/statistics', methods=['GET'])
def get_statistics():
    """
    Endpoint para obter estatísticas básicas dos dados.
    
    Returns:
        JSON com estatísticas básicas.
    """
    try:
        # Carregando e pré-processando os dados
        data = data_loader.preprocess_data()
        
        # Definindo os dados para o analisador estatístico
        stats_analyzer.set_data(data)
        
        # Obtendo estatísticas básicas para colunas numéricas relevantes
        relevant_columns = [
            'kills', 'deaths', 'assists', 'kda', 'gamelength', 
            'damagetochampions', 'dpm', 'visionscore', 'totalgold', 
            'earnedgold', 'cspm', 'dragons', 'barons'
        ]
        
        # Filtrando apenas as colunas que existem no dataset
        existing_columns = [col for col in relevant_columns if col in data.columns]
        
        # Obtendo estatísticas básicas
        basic_stats = stats_analyzer.get_basic_stats(existing_columns)
        
        # Obtendo métricas de desempenho específicas para LoL
        performance_metrics = stats_analyzer.get_performance_metrics()
        
        # Obtendo distribuição de campeões mais jogados
        champion_distribution = {}
        if 'champion' in data.columns:
            champion_distribution = stats_analyzer.get_categorical_distribution('champion')
            # Limitando para os 10 campeões mais jogados
            champion_distribution = dict(sorted(champion_distribution.items(), 
                                              key=lambda x: x[1], reverse=True)[:10])
        
        # Obtendo taxas de vitória por lado (Blue/Red)
        side_win_rates = {}
        if all(col in data.columns for col in ['side', 'result']):
            side_win_rates = stats_analyzer.calculate_win_rates('side')
        
        # Obtendo taxas de vitória por liga
        league_win_rates = {}
        if all(col in data.columns for col in ['league', 'result']):
            league_win_rates = stats_analyzer.calculate_win_rates('league')
            # Limitando para as 10 ligas com mais jogos
            league_win_rates = dict(sorted(league_win_rates.items(), 
                                         key=lambda x: x[1]['games_played'], reverse=True)[:10])
        
        # Montando a resposta
        response = {
            'status': 'success',
            'data': {
                'basic_stats': basic_stats,
                'performance_metrics': performance_metrics,
                'champion_distribution': champion_distribution,
                'side_win_rates': side_win_rates,
                'league_win_rates': league_win_rates
            }
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500
