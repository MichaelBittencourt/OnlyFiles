@echo off
echo Installing OnlyFiles...
cd /d %~dp0..
python -m pip install --upgrade pip
if errorlevel 1 (
    echo Failed to upgrade pip
    pause
    exit /b 1
)

python -m pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install requirements
    pause
    exit /b 1
)

python -m pip install -e .
if errorlevel 1 (
    echo Failed to install package
    pause
    exit /b 1
)

echo Installation completed successfully!
echo You can now use the 'onlyfiles' command.
echo To see the help, type: onlyfiles --help
pause
