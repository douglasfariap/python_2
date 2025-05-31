#!/bin/bash

# Script para executar Flask e Streamlit concorrentemente
# Este script inicia ambos os serviços em processos separados

echo "Iniciando a API Flask e a interface Streamlit concorrentemente..."

# Definindo variáveis de ambiente
export FLASK_APP=src/main.py
export FLASK_ENV=development

# Criando diretório para logs
mkdir -p logs

# Função para limpar processos ao encerrar o script
cleanup() {
    echo "Encerrando processos..."
    kill $FLASK_PID $STREAMLIT_PID 2>/dev/null
    exit 0
}

# Configurando trap para SIGINT (Ctrl+C) e SIGTERM
trap cleanup SIGINT SIGTERM

# Iniciando o servidor Flask em segundo plano
echo "Iniciando servidor Flask na porta 5000..."
cd /C/Users/dougl/OneDrive/Documentos/github/python_2/manusia && python3 -m flask run --host=0.0.0.0 --port=5000 > logs/flask.log 2>&1 &
FLASK_PID=$!

# Verificando se o Flask iniciou corretamente
sleep 2
if ! ps -p $FLASK_PID > /dev/null; then
    echo "Erro ao iniciar o servidor Flask. Verifique os logs em logs/flask.log"
    exit 1
fi

echo "Servidor Flask iniciado com PID: $FLASK_PID"

# Iniciando o Streamlit em segundo plano
echo "Iniciando interface Streamlit na porta 8501..."
cd /C/Users/dougl/OneDrive/Documentos/github/python_2/manusia && streamlit run streamlit_app/app.py --server.port=8501 --server.address=0.0.0.0 > logs/streamlit.log 2>&1 &
STREAMLIT_PID=$!

# Verificando se o Streamlit iniciou corretamente
sleep 5
if ! ps -p $STREAMLIT_PID > /dev/null; then
    echo "Erro ao iniciar o Streamlit. Verifique os logs em logs/streamlit.log"
    kill $FLASK_PID
    exit 1
fi

echo "Interface Streamlit iniciada com PID: $STREAMLIT_PID"

echo "Ambos os serviços estão em execução!"
echo "API Flask: http://localhost:5000"
echo "Interface Streamlit: http://localhost:8501"
echo ""
echo "Pressione Ctrl+C para encerrar ambos os serviços."

# Mantendo o script em execução
wait $FLASK_PID $STREAMLIT_PID
