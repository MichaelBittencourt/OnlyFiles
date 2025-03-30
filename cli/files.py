import os
import click
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich import print as rprint

console = Console()

@click.group()
def cli():
    """CLI para gerenciamento de arquivos"""
    pass

@cli.command()
@click.argument('path')
@click.option('--recursive', '-r', is_flag=True, help='Listar arquivos recursivamente')
def list(path, recursive):
    """Lista arquivos e diretórios"""
    try:
        path = Path(path)
        if not path.exists():
            console.print(f"[red]Erro: O caminho {path} não existe[/red]")
            return

        table = Table(title=f"Conteúdo de {path}")
        table.add_column("Nome", style="cyan")
        table.add_column("Tipo", style="green")
        table.add_column("Tamanho", style="yellow")
        table.add_column("Modificado", style="magenta")

        if recursive:
            for root, dirs, files in os.walk(path):
                for d in dirs:
                    full_path = Path(root) / d
                    table.add_row(
                        str(full_path.relative_to(path)),
                        "Diretório",
                        "-",
                        str(full_path.stat().st_mtime)
                    )
                for f in files:
                    full_path = Path(root) / f
                    table.add_row(
                        str(full_path.relative_to(path)),
                        "Arquivo",
                        str(full_path.stat().st_size),
                        str(full_path.stat().st_mtime)
                    )
        else:
            for item in path.iterdir():
                if item.is_dir():
                    table.add_row(
                        item.name,
                        "Diretório",
                        "-",
                        str(item.stat().st_mtime)
                    )
                else:
                    table.add_row(
                        item.name,
                        "Arquivo",
                        str(item.stat().st_size),
                        str(item.stat().st_mtime)
                    )

        console.print(table)
    except Exception as e:
        console.print(f"[red]Erro: {str(e)}[/red]")

@cli.command()
@click.argument('source')
@click.argument('destination')
def copy(source, destination):
    """Copia um arquivo ou diretório"""
    try:
        source = Path(source)
        destination = Path(destination)

        if not source.exists():
            console.print(f"[red]Erro: O arquivo/diretório fonte {source} não existe[/red]")
            return

        if source.is_file():
            import shutil
            shutil.copy2(source, destination)
            console.print(f"[green]Arquivo copiado com sucesso para {destination}[/green]")
        elif source.is_dir():
            import shutil
            shutil.copytree(source, destination)
            console.print(f"[green]Diretório copiado com sucesso para {destination}[/green]")
    except Exception as e:
        console.print(f"[red]Erro: {str(e)}[/red]")

@cli.command()
@click.argument('path')
def delete(path):
    """Remove um arquivo ou diretório"""
    try:
        path = Path(path)
        if not path.exists():
            console.print(f"[red]Erro: O arquivo/diretório {path} não existe[/red]")
            return

        if path.is_file():
            path.unlink()
            console.print(f"[green]Arquivo removido com sucesso[/green]")
        elif path.is_dir():
            import shutil
            shutil.rmtree(path)
            console.print(f"[green]Diretório removido com sucesso[/green]")
    except Exception as e:
        console.print(f"[red]Erro: {str(e)}[/red]")

@cli.command()
@click.argument('path')
def info(path):
    """Mostra informações detalhadas sobre um arquivo ou diretório"""
    try:
        path = Path(path)
        if not path.exists():
            console.print(f"[red]Erro: O arquivo/diretório {path} não existe[/red]")
            return

        stats = path.stat()
        table = Table(title=f"Informações de {path}")
        table.add_column("Propriedade", style="cyan")
        table.add_column("Valor", style="green")

        table.add_row("Nome", path.name)
        table.add_row("Caminho Absoluto", str(path.absolute()))
        table.add_row("Tipo", "Diretório" if path.is_dir() else "Arquivo")
        table.add_row("Tamanho", str(stats.st_size) if path.is_file() else "-")
        table.add_row("Criado", str(stats.st_ctime))
        table.add_row("Modificado", str(stats.st_mtime))
        table.add_row("Acessado", str(stats.st_atime))

        console.print(table)
    except Exception as e:
        console.print(f"[red]Erro: {str(e)}[/red]")

def main():
    cli()

if __name__ == '__main__':
    main() 