import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

dados ={'Ano': [2018,2019,2020,2021,2022,2023,2024],
        'Vendas': [120,152,188,200,215,212,208]}

df=pd.DataFrame(dados)

X = df[['Ano']]
y= df['Vendas']

modelo = LinearRegression()
modelo.fit(X,y)

df['Previsao'] = modelo.predict(X)

plt.figure(figsize=(8,4))
plt.plot(df['Ano'],df['Vendas'],label='Real', marker ='o')
plt.plot(df['Ano'],df['Previsao'], label='Regressão Linear' , linestyle='--')
plt.xlabel('Ano')
plt.ylabel('Vendas')
plt.title('Vendas Reais vs. Previsao')
plt.legend()
plt.tight_layout()
plt.show()

