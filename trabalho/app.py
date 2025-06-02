import streamlit as st
import DataLoader as dl
import DataAnalyzer as da
import matplotlib.pyplot as plt


# Carregamento de dados
loader = dl.DataLoader("2022_LoL_esports_match_data_from_OraclesElixir.csv")

data = loader.carregar_dados()


# Inicializa o analisador
analyzer = da.DataAnalyzer(data)

# Interface
st.title("Análise dos sados das partidas competitivas LoL Esports 2022 ")
st.sidebar.header("Filtros")

# --- Expressões Lambda para criar condições de filtro ---
# Estas lambdas recebem o DataFrame e o valor para filtrar, retornando uma Série booleana.
filter_by_liga = lambda df, liga_val: df["liga"] == liga_val
filter_by_temporada = lambda df, temporada_val: df["temporada"] == temporada_val

# --- Funções Auxiliares usando lambdas e funções de alta ordem (ex: sorted) ---
def get_available_ligas(df):
    """Retorna nomes de ligas únicos."""
    return df["liga"].unique()

def get_filtered_temporadas(df, selected_liga):
    """
    Retorna opções de 'temporada' únicas e ordenadas com base na 'liga' selecionada.
    Utiliza uma lambda para a condição de filtro e 'sorted' (HOF).
    """
    if not selected_liga: # Se nenhuma liga for selecionada, retorna lista vazia
        return []
    
    # Aplica o filtro definido pela lambda
    condition = filter_by_liga(df, selected_liga)
    filtered_df = df[condition]
    
    # Obtém temporadas únicas e as ordena (sorted é uma HOF)
    return sorted(list(filtered_df["temporada"].unique()))

def get_filtered_times(df, selected_liga, selected_temporada):
    """
    Retorna opções de 'time' únicas e ordenadas com base na 'liga' e 'temporada' selecionadas.
    Utiliza lambdas para as condições de filtro e 'sorted' (HOF).
    """
    if not selected_liga or not selected_temporada: # Se liga ou temporada não selecionadas
        return []
        
    # Aplica os filtros definidos pelas lambdas
    condition_liga = filter_by_liga(df, selected_liga)
    condition_temporada = filter_by_temporada(df, selected_temporada)
    
    combined_condition = condition_liga & condition_temporada
    filtered_df = df[combined_condition]
    
    # Obtém times únicos e os ordena
    return sorted(list(filtered_df["time"].unique()))

# --- Elementos da Interface ---

# 1. Selecionar a Liga
todas_ligas = get_available_ligas(data)
default_liga_nome = "CBLOL" # Do código original do usuário
default_liga_index = 0
if default_liga_nome in todas_ligas: # Garante que o valor padrão exista
    # .tolist() é importante se todas_ligas for um array NumPy, para usar .index()
    default_liga_index = todas_ligas.tolist().index(default_liga_nome)

liga_selecionada = st.sidebar.selectbox(
    "Selecione a Liga",
    options=todas_ligas,
    index=default_liga_index
)

# 2. Selecionar a Temporada (Split) - dependente da liga_selecionada
opcoes_temporada = get_filtered_temporadas(data, liga_selecionada)
split_selecionado = st.sidebar.selectbox(
    "Selecione a Temporada",
    options=opcoes_temporada

)

# 3. Selecionar os Times - dependente da liga_selecionada E split_selecionado
opcoes_times = get_filtered_times(data, liga_selecionada, split_selecionado)

# Determinar times selecionados por padrão
default_times_selecionados = []
if opcoes_times: # Verifica se há times para selecionar
    
    default_times_selecionados = opcoes_times[:max(len(opcoes_times),0)]

times_selecionados = st.sidebar.multiselect(
    "Selecione os times",
    options=opcoes_times,
    default=default_times_selecionados
)

# Filtragens
dados_filtrados = analyzer.filtrar_dados(times_selecionados, liga_selecionada, split_selecionado)
df_filtrado_times = dados_filtrados[dados_filtrados["posicao"] == "team"].copy()
df_filtrado_players = dados_filtrados[dados_filtrados["posicao"] != "team"].copy()
df_filtrado_grupo_times = df_filtrado_times.groupby("time").agg({"abates": "mean", "mortes": "mean", "assistencias": "mean", "ouro_total": "mean", "total_creeps": "mean"}).reset_index()

# Exibição
st.write(f"### Dados filtrados para a Liga: {liga_selecionada}, Temporada: {split_selecionado}")
df_filtrado_times = df_filtrado_times.sort_values(by="id_partida")  # Ordenando pela coluna id_partida
st.dataframe(df_filtrado_times[["id_partida", "liga", "temporada", "time", "resultado"]])


# Dados estatísticos
st.write(f"## Dados Estatísticos")
st.write(analyzer.gerar_dados_estatisticos(df_filtrado_times))


# Dados estatísticos
st.write(f"## Graficos Estatísticos")
# Gáficos

graf_dispersao=analyzer.gerar_grafico_dispersao(df_filtrado_grupo_times, "time", "abates", "Número de Abates por Partida")
st.pyplot(graf_dispersao)  # Exibe o gráfico no Streamlit


graf_desviopadrao= analyzer.gerar_grafico_media_desvio(df_filtrado_grupo_times, "time", "abates", "Média e Desvio Padrão de Abates por Time")
st.pyplot(graf_desviopadrao)  # Exibe o gráfico no Streamlit

graf_histograma = analyzer.gerar_histograma(df_filtrado_times, "abates", "Histograma de Abates das partidas")
st.pyplot(graf_histograma)  # Exibe o gráfico no Streamlit


st.write(f"#### Top 10 Picks de Campeões")
top_10_picks = df_filtrado_players["campeao"].value_counts().head(10)  
st.write(top_10_picks)  # Exibe os 10 campeões mais escolhidos
st.write(f"#### Top 10 Banimentos de Campeões")
top_10_bans = df_filtrado_times[["banimento_1", "banimento_2", "banimento_3", "banimento_4", "banimento_5"]].melt(value_name="campeao_banido")["campeao_banido"].value_counts().head(10)
st.write(top_10_bans)
st.write(f"#### Top times com mais vitórias")
top_times_vitorias = df_filtrado_times[df_filtrado_times["resultado"] == 1]["time"].value_counts().head(10)
st.write(top_times_vitorias)  # Exibe os 10 times com mais vitórias
st.write(f"#### Top times com mais derrotas")
top_times_derrotas = df_filtrado_times[df_filtrado_times["resultado"] == 0]["time"].value_counts().head(10)
st.write(top_times_derrotas)  # Exibe os 10 times com mais derrotas
