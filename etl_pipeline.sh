#!/bin/bash

# Configurações
VENV_DIR="venv"
PYTHON_SCRIPT="etl.py"
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1-2)  # Obtém 3.12

# 1. Verifica e instala os pacotes necessários
echo "Verificando dependências do sistema..."
if ! command -v python3 &> /dev/null; then
    echo "Python3 não encontrado. Instalando..."
    sudo apt update && sudo apt install -y python3
fi

# Instala o pacote específico para a versão do Python
echo "Instalando python${PYTHON_VERSION}-venv..."
sudo apt install -y "python${PYTHON_VERSION}-venv" python3-pip

# 2. Cria o ambiente virtual
echo "Criando ambiente virtual em $VENV_DIR..."
python3 -m venv "$VENV_DIR" || {
    echo "Falha ao criar ambiente virtual. Tentando método alternativo..."
    python3 -m venv --without-pip "$VENV_DIR"
    source "$VENV_DIR/bin/activate"
    curl https://bootstrap.pypa.io/get-pip.py | python
    deactivate
}

# 3. Ativa o ambiente virtual
echo "Ativando ambiente virtual..."
source "$VENV_DIR/bin/activate" || {
    echo "Falha crítica ao ativar o ambiente virtual"
    exit 1
}

# 4. Verifica se está no ambiente virtual
if [ -z "$VIRTUAL_ENV" ]; then
    echo "AVISO: Ambiente virtual pode não estar ativado corretamente"
    echo "Tentando continuando mesmo assim..."
fi

# 5. Atualiza pip
echo "Atualizando pip..."
pip install --upgrade pip

# 6. Instala dependências
if [ -f "requirements.txt" ]; then
    echo "Instalando dependências..."
    pip install -r requirements.txt
else
    echo "AVISO: Arquivo requirements.txt não encontrado"
fi

# 7. Executa o script
if [ -f "$PYTHON_SCRIPT" ]; then
    echo "Executando $PYTHON_SCRIPT..."
    python "$PYTHON_SCRIPT"
else
    echo "ERRO: Arquivo $PYTHON_SCRIPT não encontrado"
fi

# 8. Desativa o ambiente
echo "Desativando ambiente virtual..."
deactivate

echo "Processo concluído!"