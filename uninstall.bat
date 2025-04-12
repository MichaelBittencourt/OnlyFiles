@echo off
echo Desinstalando OnlyFiles...

:: Desinstala o pacote
echo Removendo OnlyFiles...
pip uninstall onlyfiles -y

:: Remove arquivos de cache
echo Limpando cache...
pip cache purge

echo.
echo Desinstalacao concluida!
pause 