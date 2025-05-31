"""
Aplicação Streamlit para visualização interativa dos dados de partidas de LoL eSports.
"""
import streamlit as st
import pandas as pd
import numpy as np
import requests
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os
import json
from PIL import Image
import io
import base64

# Adicionando o diretório raiz ao path para importar os módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.data_loader import DataLoader
from visualization.data_visualizer import DataVisualizer

# Configuração da página Streamlit
st.set_page_config(
    page_title="Análise de Dados de LoL eSports 2022",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Constantes
API_URL = "http://localhost:5000/api"
DATA_PATH = '/home/ubuntu/upload/2022_LoL_esports_match_data_from_OraclesElixir.csv'

# Função para carregar os dados localmente (para visualizações que não dependem da API)
@st.cache_data
def load_data():
    data_loader = DataLoader(DATA_PATH)
    return data_loader.preprocess_data()

# Função para obter estatísticas da API
def get_statistics():
    try:
        response = requests.get(f"{API_URL}/statistics")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Erro ao obter estatísticas: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Erro ao conectar com a API: {str(e)}")
        return None

# Função para obter um registro específico da API
def get_record(record_id):
    try:
        response = requests.get(f"{API_URL}/record/{record_id}")
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            st.warning(f"Registro com ID {record_id} não encontrado")
            return None
        else:
            st.error(f"Erro ao obter registro: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Erro ao conectar com a API: {str(e)}")
        return None

# Função para converter figura matplotlib para imagem
def fig_to_image(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    buf.seek(0)
    return Image.open(buf)

# Função para criar visualizações
def create_visualization(data, viz_type, **kwargs):
    visualizer = DataVisualizer(data)
    
    if viz_type == 'histogram':
        fig = visualizer.create_histogram(**kwargs)
    elif viz_type == 'scatter':
        fig = visualizer.create_scatter_plot(**kwargs)
    elif viz_type == 'bar':
        fig = visualizer.create_bar_chart(**kwargs)
    elif viz_type == 'heatmap':
        fig = visualizer.create_heatmap(**kwargs)
    elif viz_type == 'box':
        fig = visualizer.create_box_plot(**kwargs)
    elif viz_type == 'pie':
        fig = visualizer.create_pie_chart(**kwargs)
    else:
        st.error(f"Tipo de visualização não suportado: {viz_type}")
        return None
    
    return fig

# Título principal
st.title("Análise de Dados de LoL eSports 2022")

# Sidebar para navegação
st.sidebar.title("Navegação")
page = st.sidebar.radio(
    "Selecione uma página",
    ["Visão Geral", "Estatísticas Detalhadas", "Visualizações", "Consulta de Registros"]
)

# Carregando os dados para visualizações locais
data = load_data()

# Página: Visão Geral
if page == "Visão Geral":
    st.header("Visão Geral dos Dados")
    
    # Informações sobre o dataset
    st.subheader("Sobre o Dataset")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de Registros", f"{len(data):,}")
    with col2:
        st.metric("Número de Colunas", f"{len(data.columns):,}")
    with col3:
        st.metric("Período", f"{data['date'].min().date()} a {data['date'].max().date()}")
    
    # Estatísticas gerais da API
    st.subheader("Estatísticas Gerais")
    stats = get_statistics()
    
    if stats and stats.get('status') == 'success':
        stats_data = stats['data']
        
        # Métricas de desempenho
        st.write("#### Métricas de Desempenho")
        metrics = stats_data.get('performance_metrics', {})
        
        metric_cols = st.columns(4)
        if 'avg_kda' in metrics:
            metric_cols[0].metric("KDA Médio", f"{metrics['avg_kda']:.2f}")
        if 'avg_game_duration' in metrics:
            metric_cols[1].metric("Duração Média (min)", f"{metrics['avg_game_duration']:.2f}")
        if 'first_blood_rate' in metrics:
            metric_cols[2].metric("Taxa de First Blood", f"{metrics['first_blood_rate']:.2%}")
        if 'avg_dragons' in metrics:
            metric_cols[3].metric("Dragões por Jogo", f"{metrics['avg_dragons']:.2f}")
        
        # Distribuição de campeões
        st.write("#### Top 10 Campeões Mais Jogados")
        champion_data = stats_data.get('champion_distribution', {})
        if champion_data:
            champion_df = pd.DataFrame({
                'Campeão': list(champion_data.keys()),
                'Jogos': list(champion_data.values())
            }).sort_values('Jogos', ascending=False)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(data=champion_df, x='Campeão', y='Jogos', ax=ax)
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            st.pyplot(fig)
        
        # Taxa de vitória por lado
        st.write("#### Taxa de Vitória por Lado")
        side_data = stats_data.get('side_win_rates', {})
        if side_data:
            side_df = pd.DataFrame([
                {'Lado': side, 'Jogos': data['games_played'], 'Vitórias': data['wins'], 
                 'Taxa de Vitória': data['win_rate']}
                for side, data in side_data.items()
            ])
            
            col1, col2 = st.columns(2)
            with col1:
                st.dataframe(side_df, hide_index=True)
            
            with col2:
                fig, ax = plt.subplots(figsize=(8, 6))
                sns.barplot(data=side_df, x='Lado', y='Taxa de Vitória', ax=ax)
                ax.set_ylim(0, 1)
                ax.set_ylabel('Taxa de Vitória')
                st.pyplot(fig)
    else:
        st.warning("Não foi possível obter estatísticas da API. Verifique se o servidor Flask está em execução.")
        
        # Mostrar algumas estatísticas básicas calculadas localmente
        st.write("#### Estatísticas Básicas (Calculadas Localmente)")
        
        # KDA médio
        if all(col in data.columns for col in ['kills', 'deaths', 'assists']):
            kda = data.apply(lambda row: (row['kills'] + row['assists']) / max(1, row['deaths']), axis=1).mean()
            st.metric("KDA Médio", f"{kda:.2f}")
        
        # Duração média das partidas
        if 'gamelength' in data.columns:
            avg_duration = data['gamelength'].mean() / 60  # convertendo para minutos
            st.metric("Duração Média (min)", f"{avg_duration:.2f}")
    
    # Visualização rápida dos dados
    st.subheader("Amostra dos Dados")
    st.dataframe(data.head(10))

# Página: Estatísticas Detalhadas
elif page == "Estatísticas Detalhadas":
    st.header("Estatísticas Detalhadas")
    
    # Obtendo estatísticas da API
    stats = get_statistics()
    
    if stats and stats.get('status') == 'success':
        stats_data = stats['data']
        
        # Estatísticas básicas
        st.subheader("Estatísticas Básicas")
        basic_stats = stats_data.get('basic_stats', {})
        
        # Seleção de coluna para visualizar estatísticas
        if basic_stats:
            selected_column = st.selectbox(
                "Selecione uma coluna para ver estatísticas detalhadas",
                options=list(basic_stats.keys())
            )
            
            if selected_column in basic_stats:
                col_stats = basic_stats[selected_column]
                
                # Exibindo estatísticas em colunas
                col1, col2, col3, col4, col5 = st.columns(5)
                col1.metric("Média", f"{col_stats['mean']:.2f}")
                col2.metric("Mediana", f"{col_stats['median']:.2f}")
                col3.metric("Desvio Padrão", f"{col_stats['std']:.2f}")
                col4.metric("Mínimo", f"{col_stats['min']:.2f}")
                col5.metric("Máximo", f"{col_stats['max']:.2f}")
                
                # Histograma da coluna selecionada
                st.write(f"#### Distribuição de {selected_column}")
                fig = create_visualization(
                    data, 
                    'histogram', 
                    column=selected_column, 
                    title=f'Distribuição de {selected_column}'
                )
                st.pyplot(fig)
        
        # Taxa de vitória por liga
        st.subheader("Taxa de Vitória por Liga")
        league_data = stats_data.get('league_win_rates', {})
        if league_data:
            league_df = pd.DataFrame([
                {'Liga': league, 'Jogos': data['games_played'], 'Vitórias': data['wins'], 
                 'Taxa de Vitória': data['win_rate']}
                for league, data in league_data.items()
            ]).sort_values('Jogos', ascending=False)
            
            st.dataframe(league_df, hide_index=True)
            
            # Gráfico de barras para taxa de vitória por liga
            fig, ax = plt.subplots(figsize=(12, 6))
            sns.barplot(data=league_df, x='Liga', y='Taxa de Vitória', ax=ax)
            ax.set_ylim(0, 1)
            ax.set_ylabel('Taxa de Vitória')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            st.pyplot(fig)
    else:
        st.warning("Não foi possível obter estatísticas da API. Verifique se o servidor Flask está em execução.")
        
        # Estatísticas calculadas localmente
        st.write("#### Estatísticas Calculadas Localmente")
        
        # Seleção de coluna para visualizar estatísticas
        numeric_cols = data.select_dtypes(include=['float64', 'int64']).columns.tolist()
        selected_column = st.selectbox(
            "Selecione uma coluna para ver estatísticas detalhadas",
            options=numeric_cols
        )
        
        # Exibindo estatísticas em colunas
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Média", f"{data[selected_column].mean():.2f}")
        col2.metric("Mediana", f"{data[selected_column].median():.2f}")
        col3.metric("Desvio Padrão", f"{data[selected_column].std():.2f}")
        col4.metric("Mínimo", f"{data[selected_column].min():.2f}")
        col5.metric("Máximo", f"{data[selected_column].max():.2f}")
        
        # Histograma da coluna selecionada
        st.write(f"#### Distribuição de {selected_column}")
        fig = create_visualization(
            data, 
            'histogram', 
            column=selected_column, 
            title=f'Distribuição de {selected_column}'
        )
        st.pyplot(fig)

# Página: Visualizações
elif page == "Visualizações":
    st.header("Visualizações Interativas")
    
    # Seleção do tipo de visualização
    viz_type = st.selectbox(
        "Selecione o tipo de visualização",
        ["Histograma", "Gráfico de Dispersão", "Gráfico de Barras", "Mapa de Calor", "Box Plot", "Gráfico de Pizza"]
    )
    
    # Configurações específicas para cada tipo de visualização
    if viz_type == "Histograma":
        st.subheader("Histograma")
        
        # Seleção de coluna numérica
        numeric_cols = data.select_dtypes(include=['float64', 'int64']).columns.tolist()
        column = st.selectbox("Selecione uma coluna numérica", options=numeric_cols)
        
        # Número de bins
        bins = st.slider("Número de bins", min_value=5, max_value=100, value=30)
        
        # Criando o histograma
        fig = create_visualization(
            data, 
            'histogram', 
            column=column, 
            bins=bins, 
            title=f'Distribuição de {column}'
        )
        st.pyplot(fig)
    
    elif viz_type == "Gráfico de Dispersão":
        st.subheader("Gráfico de Dispersão")
        
        # Seleção de colunas numéricas
        numeric_cols = data.select_dtypes(include=['float64', 'int64']).columns.tolist()
        col1, col2 = st.columns(2)
        with col1:
            x_column = st.selectbox("Selecione a coluna para o eixo X", options=numeric_cols, index=0)
        with col2:
            y_column = st.selectbox("Selecione a coluna para o eixo Y", options=numeric_cols, index=1 if len(numeric_cols) > 1 else 0)
        
        # Seleção de coluna para colorir os pontos
        categorical_cols = data.select_dtypes(include=['object']).columns.tolist()
        hue_column = st.selectbox("Selecione uma coluna para colorir os pontos (opcional)", 
                                 options=["Nenhum"] + categorical_cols)
        
        # Criando o gráfico de dispersão
        fig = create_visualization(
            data, 
            'scatter', 
            x_column=x_column, 
            y_column=y_column, 
            hue_column=None if hue_column == "Nenhum" else hue_column,
            title=f'{y_column} vs {x_column}'
        )
        st.pyplot(fig)
    
    elif viz_type == "Gráfico de Barras":
        st.subheader("Gráfico de Barras")
        
        # Seleção de coluna categórica
        categorical_cols = data.select_dtypes(include=['object']).columns.tolist()
        column = st.selectbox("Selecione uma coluna categórica", options=categorical_cols)
        
        # Número de categorias a mostrar
        top_n = st.slider("Número de categorias a mostrar", min_value=5, max_value=30, value=10)
        
        # Criando o gráfico de barras
        fig = create_visualization(
            data, 
            'bar', 
            column=column, 
            top_n=top_n, 
            title=f'Top {top_n} valores de {column}'
        )
        st.pyplot(fig)
    
    elif viz_type == "Mapa de Calor":
        st.subheader("Mapa de Calor de Correlação")
        
        # Seleção de colunas numéricas
        numeric_cols = data.select_dtypes(include=['float64', 'int64']).columns.tolist()
        
        # Limitando o número de colunas para evitar mapas de calor muito grandes
        if len(numeric_cols) > 20:
            st.warning("Muitas colunas numéricas disponíveis. Selecionando apenas algumas para o mapa de calor.")
            
            # Seleção de colunas relevantes para LoL
            relevant_cols = [col for col in [
                'kills', 'deaths', 'assists', 'kda', 'gamelength', 
                'damagetochampions', 'dpm', 'visionscore', 'totalgold', 
                'earnedgold', 'cspm', 'dragons', 'barons'
            ] if col in numeric_cols]
            
            selected_cols = st.multiselect(
                "Selecione as colunas para o mapa de calor",
                options=numeric_cols,
                default=relevant_cols[:10]  # Limitando a 10 colunas por padrão
            )
        else:
            selected_cols = st.multiselect(
                "Selecione as colunas para o mapa de calor",
                options=numeric_cols,
                default=numeric_cols[:10]  # Limitando a 10 colunas por padrão
            )
        
        if selected_cols:
            # Criando o mapa de calor
            fig = create_visualization(
                data, 
                'heatmap', 
                columns=selected_cols, 
                title='Mapa de Calor de Correlação'
            )
            st.pyplot(fig)
        else:
            st.warning("Selecione pelo menos uma coluna para gerar o mapa de calor.")
    
    elif viz_type == "Box Plot":
        st.subheader("Box Plot")
        
        # Seleção de coluna numérica
        numeric_cols = data.select_dtypes(include=['float64', 'int64']).columns.tolist()
        value_column = st.selectbox("Selecione uma coluna numérica", options=numeric_cols)
        
        # Seleção de coluna categórica para agrupar
        categorical_cols = data.select_dtypes(include=['object']).columns.tolist()
        group_column = st.selectbox("Selecione uma coluna categórica para agrupar (opcional)", 
                                   options=["Nenhum"] + categorical_cols)
        
        # Criando o box plot
        fig = create_visualization(
            data, 
            'box', 
            value_column=value_column, 
            group_column=None if group_column == "Nenhum" else group_column,
            title=f'Box Plot de {value_column}'
        )
        st.pyplot(fig)
    
    elif viz_type == "Gráfico de Pizza":
        st.subheader("Gráfico de Pizza")
        
        # Seleção de coluna categórica
        categorical_cols = data.select_dtypes(include=['object']).columns.tolist()
        column = st.selectbox("Selecione uma coluna categórica", options=categorical_cols)
        
        # Número de categorias a mostrar
        top_n = st.slider("Número de categorias a mostrar", min_value=3, max_value=15, value=8)
        
        # Criando o gráfico de pizza
        fig = create_visualization(
            data, 
            'pie', 
            column=column, 
            top_n=top_n, 
            title=f'Distribuição de {column}'
        )
        st.pyplot(fig)

# Página: Consulta de Registros
elif page == "Consulta de Registros":
    st.header("Consulta de Registros")
    
    # Explicação
    st.write("""
    Nesta seção, você pode consultar informações detalhadas de um registro específico usando seu ID.
    O ID corresponde ao campo 'gameid' no dataset.
    """)
    
    # Obtenção de alguns IDs de exemplo
    sample_ids = data['gameid'].sample(5).tolist() if 'gameid' in data.columns else []
    
    # Seleção do ID
    record_id = st.text_input("Digite o ID do registro (gameid)", 
                             value=sample_ids[0] if sample_ids else "")
    
    if st.button("Consultar"):
        if record_id:
            # Obtendo o registro da API
            record_data = get_record(record_id)
            
            if record_data and record_data.get('status') == 'success':
                record = record_data['data']
                
                # Exibindo informações gerais
                st.subheader("Informações Gerais")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write("**Game ID:**", record.get('gameid', 'N/A'))
                    st.write("**Liga:**", record.get('league', 'N/A'))
                    st.write("**Data:**", record.get('date', 'N/A'))
                
                with col2:
                    st.write("**Patch:**", record.get('patch', 'N/A'))
                    st.write("**Duração (s):**", record.get('gamelength', 'N/A'))
                    st.write("**Playoffs:**", "Sim" if record.get('playoffs') else "Não")
                
                with col3:
                    st.write("**Time:**", record.get('teamname', 'N/A'))
                    st.write("**Lado:**", record.get('side', 'N/A'))
                    st.write("**Resultado:**", "Vitória" if record.get('result') == 1 else "Derrota")
                
                # Exibindo informações do jogador
                if record.get('playername'):
                    st.subheader("Informações do Jogador")
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.write("**Jogador:**", record.get('playername', 'N/A'))
                        st.write("**Posição:**", record.get('position', 'N/A'))
                        st.write("**Campeão:**", record.get('champion', 'N/A'))
                    
                    with col2:
                        st.write("**Abates:**", record.get('kills', 'N/A'))
                        st.write("**Mortes:**", record.get('deaths', 'N/A'))
                        st.write("**Assistências:**", record.get('assists', 'N/A'))
                    
                    with col3:
                        st.write("**KDA:**", f"{(record.get('kills', 0) + record.get('assists', 0)) / max(1, record.get('deaths', 1)):.2f}")
                        st.write("**Dano a Campeões:**", record.get('damagetochampions', 'N/A'))
                        st.write("**DPM:**", record.get('dpm', 'N/A'))
                    
                    with col4:
                        st.write("**Ouro Total:**", record.get('totalgold', 'N/A'))
                        st.write("**CS Total:**", record.get('total cs', 'N/A'))
                        st.write("**CSPM:**", record.get('cspm', 'N/A'))
                
                # Exibindo informações de objetivos
                st.subheader("Objetivos")
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.write("**Dragões:**", record.get('dragons', 'N/A'))
                    st.write("**Primeiro Dragão:**", "Sim" if record.get('firstdragon') else "Não")
                
                with col2:
                    st.write("**Arautos:**", record.get('heralds', 'N/A'))
                    st.write("**Primeiro Arauto:**", "Sim" if record.get('firstherald') else "Não")
                
                with col3:
                    st.write("**Barões:**", record.get('barons', 'N/A'))
                    st.write("**Primeiro Barão:**", "Sim" if record.get('firstbaron') else "Não")
                
                with col4:
                    st.write("**Torres:**", record.get('towers', 'N/A'))
                    st.write("**Primeira Torre:**", "Sim" if record.get('firsttower') else "Não")
                
                # Exibindo todos os dados em formato de tabela
                with st.expander("Ver todos os dados do registro"):
                    # Convertendo para DataFrame para melhor visualização
                    record_df = pd.DataFrame([record])
                    st.dataframe(record_df)
            else:
                st.error(f"Não foi possível encontrar o registro com ID: {record_id}")
        else:
            st.warning("Por favor, digite um ID válido.")
    
    # Exibindo alguns IDs de exemplo
    if sample_ids:
        st.write("#### IDs de Exemplo")
        st.write(", ".join(str(id) for id in sample_ids))

# Rodapé
st.markdown("---")
st.markdown("Desenvolvido para o projeto de Análise de Dados Integrada com Flask e Streamlit")
