"""
Ponto de entrada principal para a API Flask.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))  # DON'T CHANGE THIS !!!

from flask import Flask, jsonify
from src.routes.statistics import stats_bp
from src.routes.records import records_bp

app = Flask(__name__)

# Registrando os blueprints
app.register_blueprint(stats_bp, url_prefix='/api')
app.register_blueprint(records_bp, url_prefix='/api')

@app.route('/')
def index():
    """
    Rota principal da API.
    """
    return jsonify({
        'status': 'success',
        'message': 'API de Análise de Dados de LoL eSports 2022',
        'endpoints': [
            '/api/statistics',
            '/api/record/<id>'
        ]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
