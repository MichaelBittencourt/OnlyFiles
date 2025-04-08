from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name="onlyfiles",
    version="1.0.0",
    author="Grupo 05 - OnlyFiles",
    author_email="",
    description="A powerful file management and backup CLI tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MichaelBittencourt/OnlyFiles",
    packages=find_packages(include=["src", "src.*"]),
    package_dir={"": "."},
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
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "onlyfiles=src.cli.commands:cli",
        ],
    },
) 