import boto3
import os

# Definir o nome do bucket e o caminho do arquivo
bucket_name = 'raw-etl-att'
s3_file_path = 'raw_files/base01.csv'
local_file_path = '~/raw_files/base01.csv'
local_file_path = os.path.expanduser(local_file_path)

s3 = boto3.client('s3')
s3.download_file(bucket_name, s3_file_path, local_file_path)

print(f"Arquivo CSV baixado para: {local_file_path}")   
