"""
Módulo para visualização de dados de partidas de LoL eSports.
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Optional, Union, Tuple
import io
import base64
from functools import wraps


class DataVisualizer:
    """
    Classe responsável pela visualização dos dados.
    """
    
    def __init__(self, data: pd.DataFrame = None):
        """
        Inicializa o visualizador de dados.
        
        Args:
            data: DataFrame com os dados a serem visualizados.
        """
        self.data = data
        # Configurando o estilo dos gráficos
        sns.set(style="darkgrid")
        plt.rcParams.update({'font.size': 12})
    
    def set_data(self, data: pd.DataFrame) -> None:
        """
        Define o DataFrame a ser visualizado.
        
        Args:
            data: DataFrame com os dados.
        """
        self.data = data
    
    def _save_figure_to_bytes(self, fig, dpi=100):
        """
        Converte uma figura matplotlib para bytes.
        
        Args:
            fig: Figura matplotlib.
            dpi: Resolução da imagem.
            
        Returns:
            Bytes da imagem.
        """
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=dpi, bbox_inches='tight')
        buf.seek(0)
        return buf
    
    def _figure_to_base64(self, fig, dpi=100):
        """
        Converte uma figura matplotlib para base64.
        
        Args:
            fig: Figura matplotlib.
            dpi: Resolução da imagem.
            
        Returns:
            String base64 da imagem.
        """
        buf = self._save_figure_to_bytes(fig, dpi)
        return base64.b64encode(buf.getvalue()).decode('utf-8')
    
    def create_histogram(self, column: str, bins: int = 30, title: Optional[str] = None, 
                        figsize: Tuple[int, int] = (10, 6)) -> plt.Figure:
        """
        Cria um histograma para uma coluna numérica.
        
        Args:
            column: Nome da coluna.
            bins: Número de bins do histograma.
            title: Título do gráfico.
            figsize: Tamanho da figura.
            
        Returns:
            Figura matplotlib.
        """
        if self.data is None or column not in self.data.columns:
            fig, ax = plt.subplots(figsize=figsize)
            ax.text(0.5, 0.5, "Dados não disponíveis", ha='center', va='center')
            return fig
        
        # Verificando se a coluna é numérica
        if not pd.api.types.is_numeric_dtype(self.data[column]):
            fig, ax = plt.subplots(figsize=figsize)
            ax.text(0.5, 0.5, f"A coluna {column} não é numérica", ha='center', va='center')
            return fig
        
        # Criando o histograma
        fig, ax = plt.subplots(figsize=figsize)
        sns.histplot(data=self.data, x=column, bins=bins, kde=True, ax=ax)
        
        # Configurando o título
        if title:
            ax.set_title(title)
        else:
            ax.set_title(f'Distribuição de {column}')
        
        ax.set_xlabel(column)
        ax.set_ylabel('Frequência')
        
        plt.tight_layout()
        return fig
    
    def create_scatter_plot(self, x_column: str, y_column: str, hue_column: Optional[str] = None,
                          title: Optional[str] = None, figsize: Tuple[int, int] = (10, 6)) -> plt.Figure:
        """
        Cria um gráfico de dispersão entre duas colunas numéricas.
        
        Args:
            x_column: Nome da coluna para o eixo X.
            y_column: Nome da coluna para o eixo Y.
            hue_column: Nome da coluna para colorir os pontos.
            title: Título do gráfico.
            figsize: Tamanho da figura.
            
        Returns:
            Figura matplotlib.
        """
        if self.data is None or x_column not in self.data.columns or y_column not in self.data.columns:
            fig, ax = plt.subplots(figsize=figsize)
            ax.text(0.5, 0.5, "Dados não disponíveis", ha='center', va='center')
            return fig
        
        # Verificando se as colunas são numéricas
        if not (pd.api.types.is_numeric_dtype(self.data[x_column]) and 
                pd.api.types.is_numeric_dtype(self.data[y_column])):
            fig, ax = plt.subplots(figsize=figsize)
            ax.text(0.5, 0.5, "As colunas devem ser numéricas", ha='center', va='center')
            return fig
        
        # Criando o gráfico de dispersão
        fig, ax = plt.subplots(figsize=figsize)
        
        if hue_column and hue_column in self.data.columns:
            # Limitando o número de categorias para evitar gráficos sobrecarregados
            if pd.api.types.is_object_dtype(self.data[hue_column]) and self.data[hue_column].nunique() > 10:
                # Pegando as 10 categorias mais frequentes
                top_categories = self.data[hue_column].value_counts().nlargest(10).index
                plot_data = self.data[self.data[hue_column].isin(top_categories)]
                sns.scatterplot(data=plot_data, x=x_column, y=y_column, hue=hue_column, ax=ax)
                ax.text(0.5, 0.02, "Mostrando apenas as 10 categorias mais frequentes", 
                       ha='center', va='bottom', transform=ax.transAxes, fontsize=10)
            else:
                sns.scatterplot(data=self.data, x=x_column, y=y_column, hue=hue_column, ax=ax)
        else:
            sns.scatterplot(data=self.data, x=x_column, y=y_column, ax=ax)
        
        # Configurando o título
        if title:
            ax.set_title(title)
        else:
            ax.set_title(f'{y_column} vs {x_column}')
        
        ax.set_xlabel(x_column)
        ax.set_ylabel(y_column)
        
        plt.tight_layout()
        return fig
    
    def create_bar_chart(self, column: str, top_n: int = 10, title: Optional[str] = None,
                        figsize: Tuple[int, int] = (10, 6)) -> plt.Figure:
        """
        Cria um gráfico de barras para uma coluna categórica.
        
        Args:
            column: Nome da coluna.
            top_n: Número de categorias a mostrar.
            title: Título do gráfico.
            figsize: Tamanho da figura.
            
        Returns:
            Figura matplotlib.
        """
        if self.data is None or column not in self.data.columns:
            fig, ax = plt.subplots(figsize=figsize)
            ax.text(0.5, 0.5, "Dados não disponíveis", ha='center', va='center')
            return fig
        
        # Contando valores
        value_counts = self.data[column].value_counts().nlargest(top_n)
        
        # Criando o gráfico de barras
        fig, ax = plt.subplots(figsize=figsize)
        sns.barplot(x=value_counts.index, y=value_counts.values, ax=ax)
        
        # Configurando o título
        if title:
            ax.set_title(title)
        else:
            ax.set_title(f'Top {top_n} valores de {column}')
        
        ax.set_xlabel(column)
        ax.set_ylabel('Contagem')
        
        # Rotacionando os rótulos do eixo x para melhor legibilidade
        plt.xticks(rotation=45, ha='right')
        
        plt.tight_layout()
        return fig
    
    def create_heatmap(self, columns: Optional[List[str]] = None, title: Optional[str] = None,
                      figsize: Tuple[int, int] = (12, 10)) -> plt.Figure:
        """
        Cria um mapa de calor de correlação entre colunas numéricas.
        
        Args:
            columns: Lista de colunas para incluir no mapa de calor.
            title: Título do gráfico.
            figsize: Tamanho da figura.
            
        Returns:
            Figura matplotlib.
        """
        if self.data is None:
            fig, ax = plt.subplots(figsize=figsize)
            ax.text(0.5, 0.5, "Dados não disponíveis", ha='center', va='center')
            return fig
        
        # Selecionando colunas numéricas
        if columns:
            numeric_cols = [col for col in columns if col in self.data.columns and 
                           pd.api.types.is_numeric_dtype(self.data[col])]
        else:
            numeric_cols = self.data.select_dtypes(include=['float64', 'int64']).columns.tolist()
        
        # Limitando o número de colunas para evitar mapas de calor muito grandes
        if len(numeric_cols) > 20:
            numeric_cols = numeric_cols[:20]
        
        if not numeric_cols:
            fig, ax = plt.subplots(figsize=figsize)
            ax.text(0.5, 0.5, "Nenhuma coluna numérica disponível", ha='center', va='center')
            return fig
        
        # Calculando a matriz de correlação
        corr_matrix = self.data[numeric_cols].corr()
        
        # Criando o mapa de calor
        fig, ax = plt.subplots(figsize=figsize)
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5, ax=ax)
        
        # Configurando o título
        if title:
            ax.set_title(title)
        else:
            ax.set_title('Mapa de Calor de Correlação')
        
        plt.tight_layout()
        return fig
    
    def create_time_series(self, date_column: str, value_column: str, freq: str = 'M',
                          title: Optional[str] = None, figsize: Tuple[int, int] = (12, 6)) -> plt.Figure:
        """
        Cria um gráfico de série temporal.
        
        Args:
            date_column: Nome da coluna de data.
            value_column: Nome da coluna de valor.
            freq: Frequência para agrupamento ('D' para diário, 'W' para semanal, 'M' para mensal).
            title: Título do gráfico.
            figsize: Tamanho da figura.
            
        Returns:
            Figura matplotlib.
        """
        if self.data is None or date_column not in self.data.columns or value_column not in self.data.columns:
            fig, ax = plt.subplots(figsize=figsize)
            ax.text(0.5, 0.5, "Dados não disponíveis", ha='center', va='center')
            return fig
        
        # Verificando se a coluna de data é do tipo datetime
        if not pd.api.types.is_datetime64_dtype(self.data[date_column]):
            try:
                # Tentando converter para datetime
                date_series = pd.to_datetime(self.data[date_column])
            except:
                fig, ax = plt.subplots(figsize=figsize)
                ax.text(0.5, 0.5, f"A coluna {date_column} não pode ser convertida para data", 
                       ha='center', va='center')
                return fig
        else:
            date_series = self.data[date_column]
        
        # Verificando se a coluna de valor é numérica
        if not pd.api.types.is_numeric_dtype(self.data[value_column]):
            fig, ax = plt.subplots(figsize=figsize)
            ax.text(0.5, 0.5, f"A coluna {value_column} não é numérica", ha='center', va='center')
            return fig
        
        # Criando um DataFrame temporário com as colunas necessárias
        temp_df = pd.DataFrame({
            'date': date_series,
            'value': self.data[value_column]
        })
        
        # Agrupando por data e calculando a média
        time_series = temp_df.groupby(pd.Grouper(key='date', freq=freq))['value'].mean().reset_index()
        
        # Criando o gráfico de série temporal
        fig, ax = plt.subplots(figsize=figsize)
        sns.lineplot(data=time_series, x='date', y='value', marker='o', ax=ax)
        
        # Configurando o título
        if title:
            ax.set_title(title)
        else:
            ax.set_title(f'Série Temporal de {value_column}')
        
        ax.set_xlabel('Data')
        ax.set_ylabel(value_column)
        
        # Rotacionando os rótulos do eixo x para melhor legibilidade
        plt.xticks(rotation=45, ha='right')
        
        plt.tight_layout()
        return fig
    
    def create_box_plot(self, value_column: str, group_column: Optional[str] = None,
                       title: Optional[str] = None, figsize: Tuple[int, int] = (12, 6)) -> plt.Figure:
        """
        Cria um box plot para uma coluna numérica, opcionalmente agrupado por uma coluna categórica.
        
        Args:
            value_column: Nome da coluna de valor.
            group_column: Nome da coluna de agrupamento.
            title: Título do gráfico.
            figsize: Tamanho da figura.
            
        Returns:
            Figura matplotlib.
        """
        if self.data is None or value_column not in self.data.columns:
            fig, ax = plt.subplots(figsize=figsize)
            ax.text(0.5, 0.5, "Dados não disponíveis", ha='center', va='center')
            return fig
        
        # Verificando se a coluna de valor é numérica
        if not pd.api.types.is_numeric_dtype(self.data[value_column]):
            fig, ax = plt.subplots(figsize=figsize)
            ax.text(0.5, 0.5, f"A coluna {value_column} não é numérica", ha='center', va='center')
            return fig
        
        # Criando o box plot
        fig, ax = plt.subplots(figsize=figsize)
        
        if group_column and group_column in self.data.columns:
            # Limitando o número de categorias para evitar gráficos sobrecarregados
            if pd.api.types.is_object_dtype(self.data[group_column]) and self.data[group_column].nunique() > 10:
                # Pegando as 10 categorias mais frequentes
                top_categories = self.data[group_column].value_counts().nlargest(10).index
                plot_data = self.data[self.data[group_column].isin(top_categories)]
                sns.boxplot(data=plot_data, x=group_column, y=value_column, ax=ax)
                ax.text(0.5, 0.02, "Mostrando apenas as 10 categorias mais frequentes", 
                       ha='center', va='bottom', transform=ax.transAxes, fontsize=10)
            else:
                sns.boxplot(data=self.data, x=group_column, y=value_column, ax=ax)
            
            # Rotacionando os rótulos do eixo x para melhor legibilidade
            plt.xticks(rotation=45, ha='right')
        else:
            sns.boxplot(data=self.data, y=value_column, ax=ax)
        
        # Configurando o título
        if title:
            ax.set_title(title)
        else:
            if group_column:
                ax.set_title(f'Box Plot de {value_column} por {group_column}')
            else:
                ax.set_title(f'Box Plot de {value_column}')
        
        plt.tight_layout()
        return fig
    
    def create_pie_chart(self, column: str, top_n: int = 10, title: Optional[str] = None,
                        figsize: Tuple[int, int] = (10, 8)) -> plt.Figure:
        """
        Cria um gráfico de pizza para uma coluna categórica.
        
        Args:
            column: Nome da coluna.
            top_n: Número de categorias a mostrar.
            title: Título do gráfico.
            figsize: Tamanho da figura.
            
        Returns:
            Figura matplotlib.
        """
        if self.data is None or column not in self.data.columns:
            fig, ax = plt.subplots(figsize=figsize)
            ax.text(0.5, 0.5, "Dados não disponíveis", ha='center', va='center')
            return fig
        
        # Contando valores
        value_counts = self.data[column].value_counts().nlargest(top_n)
        
        # Se houver mais categorias além das top_n, agrupá-las como "Outros"
        if len(self.data[column].unique()) > top_n:
            others = pd.Series(
                [self.data[column].value_counts().sum() - value_counts.sum()], 
                index=['Outros']
            )
            value_counts = pd.concat([value_counts, others])
        
        # Criando o gráfico de pizza
        fig, ax = plt.subplots(figsize=figsize)
        ax.pie(value_counts, labels=value_counts.index, autopct='%1.1f%%', 
              startangle=90, shadow=True)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
        
        # Configurando o título
        if title:
            ax.set_title(title)
        else:
            ax.set_title(f'Distribuição de {column}')
        
        plt.tight_layout()
        return fig
    
    def create_multi_plot_dashboard(self, columns: List[str], figsize: Tuple[int, int] = (15, 12)) -> plt.Figure:
        """
        Cria um dashboard com múltiplos gráficos para as colunas especificadas.
        
        Args:
            columns: Lista de colunas para incluir no dashboard.
            figsize: Tamanho da figura.
            
        Returns:
            Figura matplotlib.
        """
        if self.data is None:
            fig, ax = plt.subplots(figsize=figsize)
            ax.text(0.5, 0.5, "Dados não disponíveis", ha='center', va='center')
            return fig
        
        # Filtrando colunas válidas
        valid_columns = [col for col in columns if col in self.data.columns]
        
        if not valid_columns:
            fig, ax = plt.subplots(figsize=figsize)
            ax.text(0.5, 0.5, "Nenhuma coluna válida especificada", ha='center', va='center')
            return fig
        
        # Determinando o layout do dashboard
        n_cols = min(3, len(valid_columns))
        n_rows = (len(valid_columns) + n_cols - 1) // n_cols
        
        # Criando a figura
        fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
        axes = axes.flatten() if n_rows * n_cols > 1 else [axes]
        
        # Criando gráficos para cada coluna
        for i, col in enumerate(valid_columns):
            if i < len(axes):
                ax = axes[i]
                
                # Verificando o tipo de dados da coluna
                if pd.api.types.is_numeric_dtype(self.data[col]):
                    # Para colunas numéricas, criar histograma
                    sns.histplot(data=self.data, x=col, kde=True, ax=ax)
                    ax.set_title(f'Distribuição de {col}')
                else:
                    # Para colunas categóricas, criar gráfico de barras
                    top_categories = self.data[col].value_counts().nlargest(10)
                    sns.barplot(x=top_categories.index, y=top_categories.values, ax=ax)
                    ax.set_title(f'Top 10 valores de {col}')
                    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
        
        # Ocultando eixos não utilizados
        for i in range(len(valid_columns), len(axes)):
            axes[i].axis('off')
        
        plt.tight_layout()
        return fig
