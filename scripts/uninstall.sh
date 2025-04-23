#!/bin/bash

echo "Uninstalling OnlyFiles..."

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Change to project directory
cd "$PROJECT_DIR"

# Remove Python package
pip3 uninstall onlyfiles -y --break-system-packages

# Find and remove system executable
EXECUTABLE_PATH=$(which onlyfiles 2>/dev/null)

if [ -n "$EXECUTABLE_PATH" ]; then
    echo "Executable found at: $EXECUTABLE_PATH"
    echo "Removing..."
    
    rm -f "$EXECUTABLE_PATH"
    
    if [ $? -ne 0 ]; then
        echo "Failed to remove executable. Trying with sudo..."
        sudo rm -f "$EXECUTABLE_PATH"
    fi
fi

# Remove additional links in common locations
echo "Cleaning executable links..."
sudo rm -f /usr/local/bin/onlyfiles
sudo rm -f /usr/bin/onlyfiles
rm -f ~/.local/bin/onlyfiles 2>/dev/null

echo "Uninstallation completed!"

# Check if the uninstallation was successful
if command -v onlyfiles &> /dev/null; then
    echo "Warning: The 'onlyfiles' command still seems to be available on the system."
    echo "Command location: $(which onlyfiles)"
    echo "Run manually: rm -f $(which onlyfiles)"
else
    echo "The 'onlyfiles' command was successfully removed from the system."
fi 