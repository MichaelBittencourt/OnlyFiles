@echo off
echo Uninstalling OnlyFiles...

:: Uninstall the package
echo Removing OnlyFiles...
pip uninstall onlyfiles -y

:: Remove cache files
echo Cleaning cache...
pip cache purge

echo.
echo Uninstallation completed!
pause 