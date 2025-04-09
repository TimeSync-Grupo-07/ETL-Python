#!/bin/bash

echo "Instalando dependências..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "Erro ao instalar dependências"
    exit 1
fi

mkdir -p ~/raw_files ~/trusted_files

if [ $? -ne 0 ]; then
    echo "Erro ao criar diretórios"
    exit 1
fi

echo "Iniciando pipeline ETL..."
echo "========================="

echo "Executando download_from_raw.py"
python3 download_from_raw.py

if [ $? -ne 0 ]; then
    echo "Erro no download_from_raw.py"
    exit 1
fi

echo "Executando data_handling.py"
python3 data_handling.py

if [ $? -ne 0 ]; then
    echo "Erro no data_handling.py"
    exit 1
fi

echo "Executando upload_to_trusted.py"
python3 upload_to_trusted.py

if [ $? -ne 0 ]; then
    echo "Erro no upload_to_trusted.py"
    exit 1
fi

echo "========================="
echo "Pipeline concluída com sucesso!"
