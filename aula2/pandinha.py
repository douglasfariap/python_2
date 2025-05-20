import pandas as pd
import matplotlib.pyplot as plt

dados ={'Ano': [2018,2019,2020,2021,2022,2023,2024],
        'Vendas': [120,152,188,200,215,212,208]}

df=pd.DataFrame(dados)


plt.plot(df['Ano'], df['Vendas'])
plt.xlabel('Ano')
plt.ylabel('Vendas')
plt.title('Vebdas por Ano')
plt.show()

