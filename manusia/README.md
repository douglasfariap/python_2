# Análise de Dados de LoL eSports 2022

Este projeto implementa uma aplicação completa de análise de dados para partidas de League of Legends eSports de 2022, integrando Flask e Streamlit para criar uma experiência interativa de visualização e análise estatística.

## Visão Geral

A aplicação foi desenvolvida seguindo os paradigmas de programação orientada a objetos e funcional, com foco em:

- **Análise estatística** de dados de partidas de LoL eSports
- **Visualizações interativas** para explorar os dados
- **API RESTful** para acesso aos dados e estatísticas
- **Interface web** para interação com os dados
- **Execução concorrente** de backend e frontend

## Estrutura do Projeto

```
lol_esports_analysis/
├── api/                  # Módulos relacionados à API
├── data/                 # Arquivos de dados
├── models/               # Classes de modelo e análise
│   ├── data_loader.py    # Carregamento e pré-processamento de dados
│   └── stats_analyzer.py # Análise estatística dos dados
├── src/                  # Código fonte da aplicação Flask
│   ├── main.py           # Ponto de entrada da API Flask
│   ├── models/           # Modelos para a API
│   ├── routes/           # Rotas da API
│   │   ├── records.py    # Endpoint para consulta de registros
│   │   └── statistics.py # Endpoint para estatísticas
│   ├── static/           # Arquivos estáticos
│   └── templates/        # Templates HTML
├── streamlit_app/        # Aplicação Streamlit
│   └── app.py            # Interface interativa
├── utils/                # Utilitários
├── visualization/        # Módulos de visualização
│   └── data_visualizer.py # Classe para visualização de dados
├── logs/                 # Logs da aplicação
├── requirements.txt      # Dependências do projeto
├── run.sh                # Script para execução concorrente
└── README.md             # Este arquivo
```

## Requisitos

- Python 3.8+
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Flask
- Streamlit
- Requests

Todas as dependências estão listadas no arquivo `requirements.txt`.

## Instalação

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd lol_esports_analysis
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Certifique-se de que o dataset está disponível em:
```
/home/ubuntu/upload/2022_LoL_esports_match_data_from_OraclesElixir.csv
```

## Execução

Para iniciar a aplicação completa (API Flask e interface Streamlit concorrentemente):

```bash
chmod +x run.sh
./run.sh
```

Isso iniciará:
- API Flask na porta 5000
- Interface Streamlit na porta 8501

Você pode acessar:
- API: http://localhost:5000
- Interface: http://localhost:8501

## Endpoints da API

### GET /api/statistics

Retorna estatísticas básicas dos dados, incluindo:
- Estatísticas descritivas (média, mediana, desvio padrão, etc.)
- Métricas de desempenho específicas para LoL
- Distribuição de campeões
- Taxas de vitória por lado e liga

Exemplo de resposta:
```json
{
  "status": "success",
  "data": {
    "basic_stats": {
      "kills": {
        "mean": 4.82,
        "median": 3.0,
        "std": 5.86,
        "min": 0,
        "max": 60,
        "count": 149232
      },
      ...
    },
    "performance_metrics": {
      "avg_kda": 5.21,
      "avg_game_duration": 31.59,
      ...
    },
    ...
  }
}
```

### GET /api/record/<id>

Retorna informações detalhadas de um registro específico com base em seu ID (gameid).

Exemplo de requisição:
```
GET /api/record/ESPORTSTMNT01_2690210
```

Exemplo de resposta:
```json
{
  "status": "success",
  "data": {
    "gameid": "ESPORTSTMNT01_2690210",
    "league": "LCK CL",
    "date": "2022-01-10 07:44:08",
    "playername": "Soboro",
    "champion": "Renekton",
    "kills": 2,
    "deaths": 3,
    "assists": 2,
    ...
  }
}
```

## Interface Streamlit

A interface Streamlit oferece uma experiência interativa para explorar os dados, com:

1. **Visão Geral**: Estatísticas gerais e informações sobre o dataset
2. **Estatísticas Detalhadas**: Análises aprofundadas com seleção de colunas
3. **Visualizações Interativas**: Gráficos personalizáveis (histogramas, dispersão, barras, etc.)
4. **Consulta de Registros**: Busca de informações detalhadas por ID

## Classes Principais

### DataLoader

Responsável pelo carregamento e pré-processamento dos dados.

```python
loader = DataLoader('/caminho/para/dataset.csv')
data = loader.preprocess_data()
```

Principais métodos:
- `load_data()`: Carrega os dados do arquivo CSV
- `preprocess_data()`: Realiza o pré-processamento dos dados
- `filter_data(filters)`: Filtra os dados com base em critérios específicos
- `get_record_by_id(record_id)`: Retorna um registro específico pelo ID

### StatsAnalyzer

Realiza análises estatísticas sobre os dados.

```python
analyzer = StatsAnalyzer(data)
stats = analyzer.get_basic_stats(['kills', 'deaths', 'assists'])
```

Principais métodos:
- `get_basic_stats(columns)`: Calcula estatísticas básicas para as colunas numéricas
- `get_correlation_matrix(columns)`: Calcula a matriz de correlação entre colunas
- `get_categorical_distribution(column)`: Calcula a distribuição de valores para uma coluna categórica
- `calculate_win_rates(group_column)`: Calcula taxas de vitória para diferentes grupos
- `get_performance_metrics()`: Calcula métricas de desempenho específicas para LoL

### DataVisualizer

Cria visualizações a partir dos dados.

```python
visualizer = DataVisualizer(data)
fig = visualizer.create_histogram('kills', title='Distribuição de Abates')
```

Principais métodos:
- `create_histogram(column, bins, title)`: Cria um histograma para uma coluna numérica
- `create_scatter_plot(x_column, y_column, hue_column)`: Cria um gráfico de dispersão
- `create_bar_chart(column, top_n, title)`: Cria um gráfico de barras para uma coluna categórica
- `create_heatmap(columns, title)`: Cria um mapa de calor de correlação
- `create_box_plot(value_column, group_column)`: Cria um box plot para uma coluna numérica

## Paradigmas de Programação

### Orientação a Objetos
- Classes bem definidas com responsabilidades específicas
- Encapsulamento de dados e comportamentos
- Reutilização de código através de métodos bem estruturados

### Programação Funcional
- Uso de funções de alta ordem como `map`, `filter` e `reduce`
- Expressões lambda para operações em dados
- Funções puras para transformações de dados

### Computação Concorrente
- Execução simultânea da API Flask e da interface Streamlit
- Comunicação em tempo real entre backend e frontend

## Contribuição

Para contribuir com este projeto:

1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Faça commit das suas alterações (`git commit -m 'Adiciona nova feature'`)
4. Faça push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para detalhes.

## Autor

Desenvolvido para o projeto de Análise de Dados Integrada com Flask e Streamlit.
