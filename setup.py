from setuptools import setup, find_packages
import os

def read_requirements():
    """Lê as dependências do arquivo requirements.txt"""
    with open('requirements.txt') as req:
        return [line.strip() for line in req if line.strip() and not line.startswith('#')]

def read_file(filename):
    """Lê o conteúdo de um arquivo"""
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()

# Garante que o help.txt está presente
help_text = """OnlyFiles - A powerful file management and backup CLI tool

Usage:
    onlyfiles <command> [options]

Commands:
    start           Launch the interactive terminal interface
    --help, -h      Show this help message
    --version       Show version information

Options:
    -d, --directory PATH    Directory to work with
    -y, --type            Organize files by type
    -v, --drives          List available drives
    -l, --logs            View operation logs
    -c, --clear-logs      Clear operation logs

Examples:
    onlyfiles start     # Start the interactive terminal interface
    onlyfiles --help    # Show this help message
    onlyfiles --version # Show version information
    onlyfiles -d /path/to/directory -y  # Organize files by type in specified directory
    onlyfiles -l                        # View operation logs

For more information, visit: https://github.com/MichaelBittencourt/OnlyFiles"""

with open('help.txt', 'w', encoding='utf-8') as f:
    f.write(help_text)

setup(
    name="onlyfiles",
    version="1.0.0",
    author="Grupo 05 - OnlyFiles",
    author_email="",
    description="A powerful file management and backup CLI tool",
    long_description=read_file('README.md'),
    long_description_content_type="text/markdown",
    url="https://github.com/MichaelBittencourt/OnlyFiles",
    packages=find_packages(include=['*']),
    include_package_data=True,
    data_files=[
        ('', ['help.txt', 'requirements.txt']),
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "onlyfiles=main:main",
        ],
    },
) 