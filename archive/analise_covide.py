import pandas as pd     
import matplotlib.pyplot as plt
import seaborn as sns



df_covid = pd.read_csv('covid_19_clean_complete.csv')

df_covid.info()
df_covid.head()
df_covid.describe()
df_covid.shape()

df_covid['Date'] = pd.to_datetime(df_covid['Date'])
df_covid['Recovered'] = df_covid['Recovered'].apply(lambda x: 0 if x < 0 else x)

df_covid['Province/State'] = df_covid['Province/State'].fillna('Unknown')

df_covid['Country/Region'].nunique()

print('Paises/Regioes unicos (primeiros 10): \n', df_covid['Country/Region'].unique()[:10])
print('\nNumeros de Regioes da OMS unicas:', df_covid['WHO Region'].nunique())
print('Regioes da OMS Unicas:\n', df_covid['WHO Region'].unique())

data_mais_recente = df_covid['Date'].max()
print('Data mais recente no dataset:', data_mais_recente)

df_ultimos_dados = df_covid[df_covid['Date'] == data_mais_recente]
df_ultimos_dados.head()

top_paises_casos = df_ultimos_dados.groupby('Country/Region') [['Confirmed', 'Deaths', 'Recovered', 'Active']].sum().sort_values(by='Confirmed', ascending=False)
print('\ntop 10 paises por casos confirmados (data mais recente):\n')
top_paises_casos = top_paises_casos.reset_index()
top_paises_casos = top_paises_casos.head(10)
top_paises_casos.head(10)


sns.set_style('whitegrid')
plt.figure(figsize=(12, 6))

# criar o grafico de barras
sns.barplot(x='Country/Region', y='Confirmed', data=top_paises_casos, palette='viridis')



plt.title('Top 10 Paises por Casos Confirmados (Data Mais Recente)', fontsize=16)
plt.xlabel('Pais/Região', fontsize=12)
plt.ylabel('Casos Confirmados', fontsize=12)


plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()