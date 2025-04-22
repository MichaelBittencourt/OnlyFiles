@echo off
echo Installing OnlyFiles...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -e .
echo Installation completed! You can now use the 'onlyfiles' command.
echo To see the help, type: onlyfiles --help
pause
