#!/bin/bash

echo "Desinstalando OnlyFiles..."

# Desinstala o pacote
echo "Removendo OnlyFiles..."
pip3 uninstall onlyfiles -y --break-system-packages

# Remove arquivos de cache
echo "Limpando cache..."
pip3 cache purge

echo
echo "Desinstalação concluída!" 