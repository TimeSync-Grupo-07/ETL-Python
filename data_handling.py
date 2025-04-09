import pandas as pd
from datetime import datetime as dt
from time import gmtime, strftime
import os

# leitura do csv como dataframe
csv_path = '~/raw_files/base01.csv'
csv_path = os.path.expanduser(csv_path)
df = pd.read_csv(csv_path)

# limpa os valores nulos do dataframe
df_nan = df.dropna()

# garante que a Data_Solicitacao seja um datetime
df_nan['Data_Solicitacao'] = pd.to_datetime(df_nan['Data_Solicitacao'], format='%d/%m/%Y')
# criando uma coluna apenas com o ano
df_nan['Ano_Solicitacao'] = df_nan['Data_Solicitacao'].dt.year

# criando um subset com as prioridades
df_prioridade = df_nan[(df_nan['Ano_Solicitacao'] > 2023) & (df_nan['Observacoes'] == 'Urgente')]

# exportando o dataframe tratado para um csv
# agora = strftime("_%Y%m%d_%H%M%S")
# csv_new_file = 'out' + agora + '.csv'
csv_new_file = 'out.csv'

# upload na pasta de trusted
csv_new_path = '~/trusted_files/'+csv_new_file
df_prioridade.to_csv(csv_new_path, index=False)

print(f".csv criado em '{csv_new_path}'\n")
