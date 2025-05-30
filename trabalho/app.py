import DataLoader
import DataAnalyzer
from fastapi import FastAPI, HTTPException
import threading
import uvicorn
import streamlit as st
import requests




# Inicialização do carregador e do analisador
# Substitua 'data.csv' pelo caminho do seu arquivo de dados
loader = DataLoader("2022_LoL_esports_match_data_from_OraclesElixir.csv")
df = loader.load_data()
analyzer = DataAnalyzer(df)

# Configuração da API RESTful com FastAPI
api = FastAPI()

@api.get("/api/statistics")
def read_statistics():
    """Retorna estatísticas básicas dos dados."""
    return analyzer.get_basic_statistics()

@api.get("/api/record/{record_id}")
def read_record(record_id: int):
    """Retorna informações detalhadas de um registro específico."""
    try:
        return analyzer.get_record(record_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# Função para executar o servidor API em segundo plano
def run_api():
    uvicorn.run(api, host="0.0.0.0", port=8000)

# Inicia a API em uma thread separada
threading.Thread(target=run_api, daemon=True).start()

# Interface com Streamlit
st.title("Dashboard de Análise de Dados")

st.header("Estatísticas Básicas")
if st.button("Carregar Estatísticas"):
    stats = requests.get("http://localhost:8000/api/statistics").json()
    st.json(stats)

st.header("Detalhes de Registro")
record_id = st.number_input("ID do Registro", min_value=0, step=1)
if st.button("Buscar Registro"):
    response = requests.get(f"http://localhost:8000/api/record/{record_id}")
    if response.status_code == 200:
        st.json(response.json())
    else:
        st.error(response.json().get("detail", "Erro ao buscar registro."))

# Observação: execute este script via `streamlit run app.py`. A API estará disponível em http://localhost:8000/api/