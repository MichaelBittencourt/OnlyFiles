@echo off
echo Uninstalling OnlyFiles...

:: Get the directory where the script is located
set "SCRIPT_DIR=%~dp0"
set "PROJECT_DIR=%SCRIPT_DIR%.."

:: Change to project directory
cd /d "%PROJECT_DIR%"

:: Uninstall the package
echo Removing OnlyFiles...
pip uninstall onlyfiles -y

:: Remove cache files
echo Cleaning cache...
pip cache purge

echo.
echo Uninstallation completed!
pause 