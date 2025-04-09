import time
from time import gmtime, strftime
import os
import boto3
import logging
import glob
import shutil

csv_path = '~/trusted_files/out.csv'
csv_path = os.path.expanduser(csv_path)

print('Carregando no bucket\n')

bucket_name = 'trusted-etl-att'
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


upload_file(csv_path, bucket_name, csv_path)
print(f"arquivo '{csv_path}' carregado em '{bucket_name}' ")
