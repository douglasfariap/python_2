import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

dados ={'Ano': [2018,2019,2020,2021,2022,2023,2024],
        'Vendas': [120,152,188,200,215,212,208]}

df=pd.DataFrame(dados)

sns.set_theme(style="whitegrid")
plt.figure(figsize=(8,4))
sns.lineplot(x='Ano', y='Vendas',data=df, marker='o')

plt.xlabel('Ano')
plt.ylabel('Vendas')
plt.title('Vendas por Ano')
plt.tight_layout()
plt.show()