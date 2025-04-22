#!/bin/bash

echo "Desinstalando OnlyFiles..."

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Change to project directory
cd "$PROJECT_DIR"

# Remove o pacote Python
pip3 uninstall onlyfiles -y --break-system-packages

# Encontra e remove o executável do sistema
EXECUTABLE_PATH=$(which onlyfiles 2>/dev/null)

if [ -n "$EXECUTABLE_PATH" ]; then
    echo "Executável encontrado em: $EXECUTABLE_PATH"
    echo "Removendo..."
    
    rm -f "$EXECUTABLE_PATH"
    
    if [ $? -ne 0 ]; then
        echo "Falha ao remover o executável. Tentando com sudo..."
        sudo rm -f "$EXECUTABLE_PATH"
    fi
fi

# Remove links adicionais em locais comuns
echo "Limpando links de executáveis..."
sudo rm -f /usr/local/bin/onlyfiles
sudo rm -f /usr/bin/onlyfiles
rm -f ~/.local/bin/onlyfiles 2>/dev/null

echo "Desinstalação concluída!"

# Verifica se a desinstalação foi bem-sucedida
if command -v onlyfiles &> /dev/null; then
    echo "Aviso: O comando 'onlyfiles' ainda parece estar disponível no sistema."
    echo "Localização do comando: $(which onlyfiles)"
    echo "Execute manualmente: rm -f $(which onlyfiles)"
else
    echo "O comando 'onlyfiles' foi removido com sucesso do sistema."
fi 