import os
import boto3
import pandas as pd
from moto import mock_s3
from etl import main

@mock_s3
def test_etl_pipeline(monkeypatch, tmp_path):
    # Criar buckets simulados
    s3 = boto3.client('s3', region_name='us-east-1')
    s3.create_bucket(Bucket='raw-etl-att')
    s3.create_bucket(Bucket='trusted-etl-att')

    # Criar CSV de teste
    test_csv = """Data_Solicitacao,Observacoes,Outros
01/01/2024,Urgente,abc
15/02/2022,Normal,def
03/03/2025,Urgente,ghi
"""
    raw_file_key = 'raw_files/base01.csv'
    s3.put_object(Bucket='raw-etl-att', Key=raw_file_key, Body=test_csv)

    # Redefinir caminhos locais usando monkeypatch (para usar tmp_path e não ~/)
    monkeypatch.setenv('HOME', str(tmp_path))  # reescreve os ~ caminhos
    
    # Executar o ETL
    main()

    # Verifica se o arquivo transformado foi salvo corretamente
    out_file = tmp_path / 'trusted_files' / 'out.csv'
    assert out_file.exists()

    df_resultado = pd.read_csv(out_file)
    assert len(df_resultado) == 2
    assert 'Ano_Solicitacao' in df_resultado.columns
    assert all(df_resultado['Observacoes'] == 'Urgente')
    assert all(df_resultado['Ano_Solicitacao'] > 2023)
