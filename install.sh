#!/bin/bash

echo "Installing OnlyFiles..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python not found. Please install Python 3.8 or higher."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "Pip not found. Please install pip3."
    exit 1
fi

# Install dependencies
echo "Installing dependencies..."
pip3 install -r requirements.txt --break-system-packages

# Install the package
echo "Installing OnlyFiles..."
pip3 install . --break-system-packages

echo
echo "Installation completed! You can now use the 'onlyfiles' command."
echo "To see the help, type: onlyfiles --help"