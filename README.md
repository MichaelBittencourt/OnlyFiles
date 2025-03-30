# OnlyFiles

This project was created to help users to organize the files in their workspace

# CLI (Command Line Interface)
## Ativando o ambiente virtual

Para ativar o ambiente virtual, siga os passos:

1. Crie o ambiente virtual:
```bash
python -m venv venv
```

2. Ative o ambiente virtual:
- No Linux/Mac:
```bash
source venv/bin/activate
```
- No Windows:
```bash
.\venv\Scripts\activate
```

**Importante**: Você DEVE ativar o ambiente virtual antes de usar qualquer comando do CLI. Você saberá que o ambiente virtual está ativo quando ver `(venv)` no início do seu prompt.

## Lista de comandos:

### 1. Listar Arquivos (`list`)
Lista todos os arquivos e diretórios em um caminho específico.

```bash
files list <caminho> [--recursive]
```

Opções:
- `--recursive` ou `-r`: Lista arquivos recursivamente em subdiretórios

Exemplo:
```bash
# Listar arquivos no diretório atual
files list .

# Listar arquivos recursivamente
files list . --recursive
```

### 2. Copiar Arquivos/Diretórios (`copy`)
Copia um arquivo ou diretório para um novo local.

```bash
files copy <origem> <destino>
```

Exemplo:
```bash
# Copiar um arquivo
files copy documento.txt backup/documento.txt

# Copiar um diretório
files copy pasta backup/pasta
```

### 3. Deletar Arquivos/Diretórios (`delete`)
Remove um arquivo ou diretório.

```bash
files delete <caminho>
```

Exemplo:
```bash
# Deletar um arquivo
files delete arquivo.txt

# Deletar um diretório
files delete pasta
```

### 4. Informações Detalhadas (`info`)
Mostra informações detalhadas sobre um arquivo ou diretório, incluindo:
- Nome
- Caminho absoluto
- Tipo (arquivo ou diretório)
- Tamanho (para arquivos)
- Data de criação
- Data de modificação
- Data de último acesso

```bash
files info <caminho>
```

Exemplo:
```bash
# Ver informações de um arquivo
files info documento.txt

# Ver informações de um diretório
files info pasta
```
