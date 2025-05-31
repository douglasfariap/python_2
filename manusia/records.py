"""
Rotas para consulta de registros específicos da API.
"""
from flask import Blueprint, jsonify, request
import pandas as pd
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from models.data_loader import DataLoader

# Criando o blueprint
records_bp = Blueprint('records', __name__)

# Caminho para o dataset
DATA_PATH = '/home/ubuntu/upload/2022_LoL_esports_match_data_from_OraclesElixir.csv'

# Instanciando o carregador de dados
data_loader = DataLoader(DATA_PATH)

@records_bp.route('/record/<id>', methods=['GET'])
def get_record(id):
    """
    Endpoint para obter informações detalhadas de um registro específico.
    
    Args:
        id: ID do registro a ser buscado.
        
    Returns:
        JSON com os dados do registro.
    """
    try:
        # Carregando e pré-processando os dados se ainda não foi feito
        if data_loader.data is None:
            data_loader.preprocess_data()
        
        # Buscando o registro pelo ID
        record = data_loader.get_record_by_id(id)
        
        if record is None:
            return jsonify({
                'status': 'error',
                'message': f'Registro com ID {id} não encontrado'
            }), 404
        
        # Convertendo valores numpy para tipos Python nativos para serialização JSON
        for key, value in record.items():
            if pd.isna(value):
                record[key] = None
            elif isinstance(value, (pd.Timestamp, pd.Timedelta)):
                record[key] = str(value)
            elif hasattr(value, 'dtype'):
                record[key] = value.item()
        
        # Montando a resposta
        response = {
            'status': 'success',
            'data': record
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500
