import pandas as pd
from datetime import datetime as dt
import os
import boto3
import logging
from botocore.exceptions import ClientError
from time import gmtime, strftime

print("Iniciando processo de ETL...")

raw_bucket_name = 'raw-etl-att'
s3_file_path = 'raw_files/base01.csv'
local_raw_path = '~/raw_files/base01.csv'
local_raw_path = os.path.expanduser(local_raw_path)

os.makedirs(os.path.dirname(local_raw_path), exist_ok=True)

print(f"Baixando arquivo do bucket {raw_bucket_name}...")
s3 = boto3.client('s3')
try:
    s3.download_file(raw_bucket_name, s3_file_path, local_raw_path)
    print(f"Arquivo CSV baixado para: {local_raw_path}")
except Exception as e:
    print(f"Erro ao baixar arquivo: {e}")
    exit()

df = pd.read_csv(local_raw_path)
df_nan = df.dropna()
df_nan['Data_Solicitacao'] = pd.to_datetime(df_nan['Data_Solicitacao'], format='%d/%m/%Y')
df_nan['Ano_Solicitacao'] = df_nan['Data_Solicitacao'].dt.year
df_prioridade = df_nan[(df_nan['Ano_Solicitacao'] > 2023) & (df_nan['Observacoes'] == 'Urgente')]

csv_new_file = 'out.csv'
trusted_local_path = '~/trusted_files/' + csv_new_file
trusted_local_path = os.path.expanduser(trusted_local_path)
os.makedirs(os.path.dirname(trusted_local_path), exist_ok=True)
df_prioridade.to_csv(trusted_local_path, index=False)
print(f".csv criado em '{trusted_local_path}'\n")

trusted_bucket_name = 'trusted-etl-att'
def upload_file(file_name, bucket, object_name=None):
    if object_name is None:
        object_name = os.path.basename(file_name)
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

print('Carregando no bucket\n')
upload_file(trusted_local_path, trusted_bucket_name, csv_new_file)
print(f"arquivo '{csv_new_file}' carregado em '{trusted_bucket_name}'")