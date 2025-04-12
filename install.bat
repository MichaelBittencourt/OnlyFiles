@echo off
echo Instalando OnlyFiles...

:: Verifica se o Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo Python nao encontrado. Por favor, instale o Python 3.8 ou superior.
    exit /b 1
)

:: Instala as dependências
echo Instalando dependencias...
pip install -r requirements.txt

:: Instala o pacote
echo Instalando OnlyFiles...
pip install .

echo.
echo Instalacao concluida! Voce pode usar o comando 'onlyfiles' agora.
echo Para ver a ajuda, digite: onlyfiles --help
pause 