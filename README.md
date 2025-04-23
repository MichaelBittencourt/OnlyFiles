# OnlyFiles

A powerful command-line file management and organization tool.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🇺🇸 English

### Overview

OnlyFiles is a command-line utility designed to help you organize files systematically. It offers various file organization methods (by extension, date, size, and type), backup capabilities, and an interactive terminal interface.

### Features

- **Multiple Organization Methods**:
  - By extension - Group files with the same extension
  - By date - Organize files into folders by creation/modification date
  - By size - Categorize files into size-based folders (small, medium, large)
  - By type - Sort files into predefined categories (documents, images, videos, music)

- **File Management**:
  - Create backups of organized files
  - Restore from backups
  - View detailed operation logs
  - Interactive terminal interface

- **Supported File Types**:
  - **Images**: .jpg, .jpeg, .png, .gif, .bmp, .tiff, .svg, .webp
  - **Documents**: .pdf, .txt, .docx, .doc, .xls, .xlsx, .ppt, .pptx, .odt, .md
  - **Music**: .mp3, .wav, .aac, .flac, .ogg, .m4a
  - **Videos**: .mp4, .mkv, .avi, .mov, .wmv, .flv, .webm
  - **Others**: Any extension not in the categories above

### Installation

#### Using pip

```bash
pip install onlyfiles
```

#### From source

```bash
# Clone the repository
git clone https://github.com/MichaelBittencourt/OnlyFiles.git
cd OnlyFiles

# Install using the provided script
# On Linux/macOS:
./scripts/install.sh

# On Windows:
scripts\install.bat
```

### Usage

OnlyFiles can be used both as a command-line tool and through an interactive terminal interface.

#### Command Line Interface

```bash
# Basic help
onlyfiles --help

# Organize files by extension in the specified directory
onlyfiles --directory /path/to/directory --extension

# Organize files by type
onlyfiles --directory /path/to/directory --type

# Create a backup before organizing
onlyfiles --directory /path/to/directory --backup

# View operation logs
onlyfiles --logs

# Clear logs
onlyfiles --clear-logs
```

#### Interactive Interface

```bash
# Start the interactive interface
onlyfiles start
```

The interactive interface provides a user-friendly menu to:
- Organize files in the current or another directory
- View supported file categories
- Access and manage operation logs
- Restore files from previous operations

### Architecture

OnlyFiles is built with a modular architecture:

- **CLI Module** (`cli/`): Handles command-line arguments and interactive interface
- **Core Module** (`core/`): Implements file management and organization logic
- **Utils Module** (`utils/`): Contains utilities like logging and help text management

### Requirements

- Python 3.8 or higher
- Dependencies:
  - click
  - rich
  - typing-extensions

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🇧🇷 Português (Brasil)

### Visão Geral

OnlyFiles é uma ferramenta de linha de comando projetada para ajudar na organização sistemática de arquivos. Oferece vários métodos de organização (por extensão, data, tamanho e tipo), recursos de backup e uma interface interativa de terminal.

### Funcionalidades

- **Múltiplos Métodos de Organização**:
  - Por extensão - Agrupa arquivos com a mesma extensão
  - Por data - Organiza arquivos em pastas por data de criação/modificação
  - Por tamanho - Categoriza arquivos em pastas baseadas em tamanho (pequeno, médio, grande)
  - Por tipo - Classifica arquivos em categorias predefinidas (documentos, imagens, vídeos, música)

- **Gerenciamento de Arquivos**:
  - Cria backups dos arquivos organizados
  - Restaura a partir de backups
  - Visualiza logs detalhados de operações
  - Interface interativa de terminal

- **Tipos de Arquivos Suportados**:
  - **Imagens**: .jpg, .jpeg, .png, .gif, .bmp, .tiff, .svg, .webp
  - **Documentos**: .pdf, .txt, .docx, .doc, .xls, .xlsx, .ppt, .pptx, .odt, .md
  - **Música**: .mp3, .wav, .aac, .flac, .ogg, .m4a
  - **Vídeos**: .mp4, .mkv, .avi, .mov, .wmv, .flv, .webm
  - **Outros**: Qualquer extensão não listada nas categorias acima

### Instalação

#### Usando pip

```bash
pip install onlyfiles
```

#### A partir do código-fonte

```bash
# Clone o repositório
git clone https://github.com/MichaelBittencourt/OnlyFiles.git
cd OnlyFiles

# Instale usando o script fornecido
# No Linux/macOS:
./scripts/install.sh

# No Windows:
scripts\install.bat
```

### Uso

OnlyFiles pode ser usado tanto como uma ferramenta de linha de comando quanto através de uma interface interativa de terminal.

#### Interface de Linha de Comando

```bash
# Ajuda básica
onlyfiles --help

# Organizar arquivos por extensão no diretório especificado
onlyfiles --directory /caminho/para/diretorio --extension

# Organizar arquivos por tipo
onlyfiles --directory /caminho/para/diretorio --type

# Criar um backup antes de organizar
onlyfiles --directory /caminho/para/diretorio --backup

# Visualizar logs de operações
onlyfiles --logs

# Limpar logs
onlyfiles --clear-logs
```

#### Interface Interativa

```bash
# Iniciar a interface interativa
onlyfiles start
```

A interface interativa fornece um menu amigável para:
- Organizar arquivos no diretório atual ou em outro diretório
- Visualizar categorias de arquivos suportadas
- Acessar e gerenciar logs de operações
- Restaurar arquivos de operações anteriores

### Arquitetura

OnlyFiles é construído com uma arquitetura modular:

- **Módulo CLI** (`cli/`): Gerencia argumentos de linha de comando e interface interativa
- **Módulo Core** (`core/`): Implementa a lógica de gerenciamento e organização de arquivos
- **Módulo Utils** (`utils/`): Contém utilitários como logging e gerenciamento de texto de ajuda

### Requisitos

- Python 3.8 ou superior
- Dependências:
  - click
  - rich
  - typing-extensions

### Licença

Este projeto está licenciado sob a Licença MIT - consulte o arquivo [LICENSE](LICENSE) para obter detalhes.

![Demonstração do OnlyFiles](https://imgur.com/a/i7bGa33)
