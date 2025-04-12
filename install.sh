#!/bin/bash

echo "Instalando OnlyFiles..."

# Verifica se o Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "Python não encontrado. Por favor, instale o Python 3.8 ou superior."
    exit 1
fi

# Verifica se o pip está instalado
if ! command -v pip3 &> /dev/null; then
    echo "Pip não encontrado. Por favor, instale o pip3."
    exit 1
fi

# Instala as dependências
echo "Instalando dependências..."
pip3 install -r requirements.txt --break-system-packages

# Instala o pacote
echo "Instalando OnlyFiles..."
pip3 install . --break-system-packages

echo
echo "Instalação concluída! Você pode usar o comando 'onlyfiles' agora."
echo "Para ver a ajuda, digite: onlyfiles --help"