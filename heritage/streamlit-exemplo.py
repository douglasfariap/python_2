import streamlit as st
import pandas as pd
import plotly.express as px

data= pd.read_csv("34_years_world_export_import_dataset.csv")
data.columns = data.columns.str.strip()

data.rename(columns={
    'Partner Name': 'País',
    'Year': 'Ano',
    'Export (US$ Thousand)': 'Exportação',
    'Import (US$ Thousand)': 'Importação'
}, inplace=True)

st.title("Análise de Exportacoes e Importações Mundiais")
st.sidebar.header("Filtros")
paises_selecionados = st.sidebar.multiselect(
    "Selecione os Países",
    options=data["País"].unique(),
    default=data["País"].unique()[:3]
)

ano_selecionado = st.sidebar.selectbox(
    "Selecione o Ano",
    options= sorted(data["Ano"].unique(), reverse=True)
)

valor_tipo = st.sidebar.radio(
    "Tipo de Valor",
    options=["Exportação", "Importação"]
)

dados_filtrados= data[
    (data["País"].isin(paises_selecionados)) &
    (data["Ano"]== ano_selecionado)
].copy()

#exibir tabela
st.write(f"### {valor_tipo} em {ano_selecionado} para os paises selecionados")
st.dataframe(dados_filtrados[["País", "Ano", valor_tipo]])

fig_bar = px.bar(
    dados_filtrados,
    x="País",
    y=valor_tipo,
    color="País",
    title=f"{valor_tipo} Por País - {ano_selecionado}",
    labels={ valor_tipo: "Valor ( US$ Milhares)"}
)

st.plotly_chart(fig_bar)

dados_historico = data[
    (data["País"].isin(paises_selecionados))
].groupby(["Ano","País"])[valor_tipo].sum().reset_index()

fig_line= px.line(
    dados_historico,
    x="Ano",
    y=valor_tipo,
    color="País",
    title=f"Evolucao Hisórica de {valor_tipo} por País",
    markers=True,
    labels={valor_tipo: "Valor (US$ Milhares)"}
)
st.plotly_chart(fig_line)

st.write("Aplicação desenvolvida com Streamlit, Pandas e Plotly")