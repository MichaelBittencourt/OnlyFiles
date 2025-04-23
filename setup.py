from setuptools import setup, find_packages
import os

def read_requirements():
    """Reads dependencies from requirements.txt file"""
    with open('requirements.txt', 'r') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

def read_file(filename):
    """Reads the content of a file"""
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()

# Read the content of help.txt file
def read_help_file():
    help_file_path = os.path.join(os.path.dirname(__file__), 'docs', 'help.txt')
    with open(help_file_path, 'r', encoding='utf-8') as f:
        return f.read()

setup(
    name="onlyfiles",
    version="1.0.0",
    author="Grupo 05 - OnlyFiles",
    author_email="",
    description="A powerful file management and backup CLI tool",
    long_description=read_help_file(),
    long_description_content_type="text/plain",
    url="https://github.com/MichaelBittencourt/OnlyFiles",
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    include_package_data=True,
    package_data={
        'onlyfiles': ['docs/*.txt'],
    },
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
            "onlyfiles=onlyfiles.main:main",
        ],
    },
) 