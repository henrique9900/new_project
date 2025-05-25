import pandas as pd
import sqlite3

#Faz a leitura dos arquivos(conecção)
df_2000 = pd.read_csv('gasolina_2000+.csv', index_col=0)
df_2010 = pd.read_csv('gasolina_2010+.csv', index_col=0)

#combinação dos dados
df_combined = pd.concat([df_2000, df_2010], ignore_index=True)

#head tras as 5 primeiras linhas e info tras um resumo das colunas se ha valores nulos
df_combined.head(3)
#esse info tras todas as colunas e os tipos de dados visualizado
df_combined.info()
#ve os 5 principais()
df_combined.tail(5)

df_combined['MARGEM MÉDIA REVENDA'] [0]

type(df_combined['DATA INICIAL'] [2])

#to datetime converte para datetime para poder fazer filtros
df_combined["DATA INICIAL"] = pd.to_datetime(df_combined["DATA INICIAL"])
df_combined["DATA FINAL"] = pd.to_datetime(df_combined["DATA FINAL"])

#CRIA UMA NOVA COLUNA E COLOCA NO FORMATO MMM E AAA USANDO O LAMBDA
df_combined["ANO-MES"] = df_combined["DATA FINAL"].apply(lambda x: f"{x.year}/{x.month:02d}")
#LISTAR USANDO O VALUE COUNTS TODOS OS PRODUDOS DA BASE DE DADOS
df_combined.columns
df_combined["PRODUTO"].value_counts()

#filtra os preços da gasolina comum usando a tabela produto
df5 = df_combined[df_combined['PRODUTO'] == 'GASOLINA COMUM']

#preço medio de revenda da gasolina em agosto de 2008?

df5[df5['ANO-MES'] == '2008/08'] ['PREÇO MÉDIO REVENDA'].mean()

#preço medio da gasolina em SP filtrado usando parentese.
df5[(df5['ANO-MES'] == '2014/05') & (df5['ESTADO'] == 'SAO PAULO')] ['PREÇO MÉDIO REVENDA'].mean()
#aqui é filtrado o preço da gasolina quando passado de 5
#PASSAR UMA LISTA [] DENTRO DO FILTRO[] E SELECIONAR AS COLUNAS DE INTERESSE
df5[df5['PREÇO MÉDIO REVENDA'] > 5][["ESTADO", "ANO-MES", "PREÇO MÉDIO REVENDA"]].head(20)

#qual a media de preços dos estados da regiao sul EM 2012/ FILTRADO PELO ANO
df_aux = df5[df5["DATA FINAL"].apply(lambda x: x.year) == 2012]
#FILTRADO JA PELA REGIAO SUL
df_aux[df_aux["REGIÃO"] == "SUL"] ["PREÇO MÉDIO REVENDA"].mean()

#OBTER UMA TABELA CONTENDO VARIAÇAO PERCENTUAL ANO A ANO PARA O ESTADO DO RIO DE JANEIRO
df5["MES"] = df5["DATA FINAL"].apply(lambda x: x.month)
df_rio = df5[df5["ESTADO"] == "RIO DE JANEIRO"]

df_month_rio = df_rio.groupby("ANO-MES") [["PREÇO MÉDIO REVENDA", "MES"]].last()
df_month_rio[df_month_rio["MES"] == 12]
 #criando nova variavel e fazendo um agrupamento no df original
df_max = df5.groupby("ANO-MES").max() ["PREÇO MÉDIO REVENDA"]

df_min = df5.groupby("ANO-MES").min() ["PREÇO MÉDIO REVENDA"]


df_diff = pd.DataFrame()

df_diff["abs_diff"] = df_max - df_min
df_diff["percent_diff"] = (df_max - df_min) / df_min * 100

idx_max = df5.groupby("ANO-MES") ["PREÇO MÉDIO REVENDA"].idxmax()
idx_min = df5.groupby("ANO-MES") ["PREÇO MÉDIO REVENDA"].idxmin()
#cria uma nova coluna com os novos indices max e min()
df_diff["max"] = df_max
df_diff["min"] = df_min


df5.loc[idx_max, :]["ESTADO"].values

df_diff["ESTADO_MAX"] = df5.loc[idx_max, :]["ESTADO"].values
df_diff["ESTADO_MIN"] = df5.loc[idx_min, :]["ESTADO"].values


df_diff["ESTADO_MAX"].value_counts()