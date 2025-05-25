mensagem = "oi"
print(mensagem)

#to datetime converte para datetime para poder fazer filtros
df_combined["DATA INICIAL"] = pd.to_datetime(df_combined["DATA INICIAL"])
df_combined["DATA FINAL"] = pd.to_datetime(df_combined["DATA FINAL"])

#CRIA UMA NOVA COLUNA E COLOCA NO FORMATO MMM E AAA USANDO O LAMBDA
df_combined["ANO-MES"] = df_combined["DATA FINAL"].apply(lambda x: f"{x.year}/{x.month:02d}")
#LISTAR USANDO O VALUE COUNTS TODOS OS PRODUDOS DA BASE DE DADOS
df_combined.columns
df_combined["PRODUTO"].value_counts() #novo comentario adicionado