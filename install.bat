@echo off
echo Installing OnlyFiles...

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python not found. Please install Python 3.8 or higher.
    exit /b 1
)

:: Check if pip is installed
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Pip not found. Please install pip.
    exit /b 1
)

:: Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

:: Install the package
echo Installing OnlyFiles...
pip install .

echo.
echo Installation completed! You can now use the 'onlyfiles' command.
echo To see the help, type: onlyfiles --help
pause 