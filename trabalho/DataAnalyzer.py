import plotly.express as px
import matplotlib.pyplot as plt

class DataAnalyzer:
    def __init__(self, data):
        self.data = data

    def filtrar_dados(self, time, liga, split):
        return self.data[
            (self.data["time"].isin(time)) &
            (self.data["liga"]== liga) &
            (self.data["temporada"] == split)
        ].copy()
   

    def gerar_dados_estatisticos(self, dados_filtrados):
        estatisticas = {
            "Média de Abates": dados_filtrados["abates"].mean().round(2),
            "Média de Mortes": dados_filtrados["mortes"].mean().round(2),
            "Média de Assistências": dados_filtrados["assistencias"].mean().round(2),
            "Média de Ouro Total": dados_filtrados["ouro_total"].mean().round(2),
            "Média de Creeps Abatidos": dados_filtrados["total_creeps"].mean().round(2),
            "Desvio Padrão de Abates": dados_filtrados["abates"].std().round(2),
            "Desvio Padrão de Mortes": dados_filtrados["mortes"].std().round(2),
            "Desvio Padrão de Assistências": dados_filtrados["assistencias"].std().round(2),
            "Desvio Padrão de Ouro Total": dados_filtrados["ouro_total"].std().round(2),
            "Desvio Padrão de Creeps Abatidos": dados_filtrados["total_creeps"].std().round(2),
            "Mediana de Abates": dados_filtrados["abates"].median().round(2),
            "Mediana de Mortes": dados_filtrados["mortes"].median().round(2),
            "Mediana de Assistências": dados_filtrados["assistencias"].median().round(2),
            "Mediana de Ouro Total": dados_filtrados["ouro_total"].median().round(2),
            "Mediana de Creeps Abatidos": dados_filtrados["total_creeps"].median().round(2),

        } 
        return estatisticas
          
    def gerar_grafico_dispersao(self, dados_filtrados, x_coluna, y_coluna, titulo):
        fig, ax = plt.subplots(figsize=(15, 5))

        ax.scatter(dados_filtrados[x_coluna], dados_filtrados[y_coluna], alpha=0.7, edgecolors="black")

        ax.set_title(titulo)
        ax.set_xlabel(x_coluna)
        ax.set_ylabel(y_coluna)
        ax.grid(True, linestyle='--', alpha=0.2)

        plt.tight_layout()
        return fig
    
    def gerar_grafico_media_desvio(self, dados_filtrados, grupo, coluna_valor, titulo):
         # Agrupamento por categoria
        estatisticas = dados_filtrados.groupby(grupo)[coluna_valor].agg(['mean', 'std']).reset_index()
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(
            estatisticas[grupo],
            estatisticas["mean"],
            yerr=estatisticas["std"],  # desvio padrão como linha de erro
            capsize=5,
            color="skyblue",
            edgecolor="black"
        )

        ax.set_title(titulo)
        ax.set_ylabel("Média de " + coluna_valor)
        ax.set_xlabel(grupo)
        ax.grid(axis="y", linestyle="--", alpha=0.5)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        return fig
    
    def gerar_histograma(self, dados, coluna, titulo, bins=20):
        fig, ax = plt.subplots(figsize=(10, 6))

        ax.hist(dados[coluna].dropna(), bins=bins, color="skyblue", edgecolor="black", alpha=0.7)

        ax.set_title(titulo)
        ax.set_xlabel(coluna)
        ax.set_ylabel("Frequência")
        ax.grid(True, linestyle='--', alpha=0.5)

        plt.tight_layout()
        return fig
'''
    def gerar_grafico_linhas(self, paises, valor_tipo):
        dados_historico = self.data[
            self.data["País"].isin(paises)
        ].groupby(["Ano", "País"])[valor_tipo].sum().reset_index()

        fig = px.line(
            dados_historico,
            x="Ano",
            y=valor_tipo,
            color="País",
            title=f"Evolução Histórica de {valor_tipo} por País",
            markers=True,
            labels={valor_tipo: "Valor (US$ Milhares)"}
        )
        return fig
''';