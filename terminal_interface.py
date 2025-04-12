import os
import sys
import shutil
from rich.console import Console
from rich.panel import Panel
from logger import Logger
from Execution import Execution

console = Console()

class TerminalInterface:
    """Provides a terminal-based user interface for file organization operations."""
    
    def __init__(self):
        self.current_path = os.getcwd()
        self.logger = Logger("TerminalInterface", True)
        self.execution = Execution(self.logger)

    def clear_screen(self):
        """Clears the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_header(self):
        """Displays the application header."""
        console.print(Panel.fit(
            "[bold blue]File Organizer[/bold blue]",
            title="File Organizer",
            border_style="blue"
        ))

    def display_categories(self):
        """Displays supported categories."""
        console.print(Panel.fit(
            "[bold blue]Supported Categories[/bold blue]\n\n"
            "[green]Imagens:[/green] .jpg, .jpeg, .png, .gif, .bmp, .tiff, .svg, .webp\n"
            "[green]Documentos:[/green] .pdf, .txt, .docx, .doc, .xls, .xlsx, .ppt, .pptx, .odt, .md\n"
            "[green]Músicas:[/green] .mp3, .wav, .aac, .flac, .ogg, .m4a\n"
            "[green]Vídeos:[/green] .mp4, .mkv, .avi, .mov, .wmv, .flv, .webm\n"
            "[green]Outros:[/green] Qualquer extensão não listada acima",
            title="Categories",
            border_style="blue"
        ))

    def display_menu(self):
        """Displays the main menu."""
        console.print("\n[bold]Options:[/bold]")
        console.print("1. Organize files in current folder")
        console.print("2. Organize files in another folder")
        console.print("3. View supported categories")
        console.print("4. View logs")
        console.print("5. Exit")
        print()

    def get_user_choice(self):
        """Gets user choice."""
        while True:
            try:
                choice = input("Choose an option [1/2/3/4/5]: ")
                if choice in ['1', '2', '3', '4', '5']:
                    return choice
                console.print("[red]Invalid option. Please choose between 1 and 5.[/red]")
            except KeyboardInterrupt:
                print("\nOperation cancelled by user.")
                sys.exit(0)

    def organize_current_directory(self):
        """Organizes files in the current directory."""
        console.print(f"\n[bold]Organizing files in:[/bold] {self.current_path}")
        try:
            self.execution.organize_all(self.current_path)
            console.print("[green]Files organized successfully![/green]")
        except Exception as e:
            error_msg = f"Error organizing files: {str(e)}"
            console.print(f"[red]{error_msg}[/red]")
            self.logger.error(error_msg)
        input("\nPress Enter to continue...")

    def list_directory_contents(self, path):
        """Lista o conteúdo de um diretório."""
        try:
            items = os.listdir(path)
            dirs = []
            files = []
            
            for item in items:
                full_path = os.path.join(path, item)
                if os.path.isdir(full_path):
                    dirs.append(item)
                else:
                    files.append(item)
            
            return sorted(dirs), sorted(files)
        except Exception as e:
            console.print(f"[red]Erro ao listar diretório: {str(e)}[/red]")
            return [], []

    def show_directory_navigation(self, current_path):
        """Mostra navegação interativa do diretório."""
        self.clear_screen()
        console.print(f"\n[bold blue]Caminho atual:[/bold blue] {current_path}")
        console.print("\n[bold yellow]Diretórios disponíveis:[/bold yellow]")
        
        dirs, files = self.list_directory_contents(current_path)
        
        # Listar diretórios
        for i, dir_name in enumerate(dirs, 1):
            console.print(f"{i}. 📁 {dir_name}")
        
        # Listar arquivos
        if files:
            console.print("\n[bold yellow]Arquivos:[/bold yellow]")
            for file in files:
                name, ext = os.path.splitext(file)
                if ext:  # Se tiver extensão
                    console.print(f"   📄 {name} ({ext})")
                else:  # Se não tiver extensão
                    console.print(f"   📄 {file}")
        
        # Opções
        console.print("\n[bold]Opções:[/bold]")
        console.print("B - Voltar ao diretório anterior")
        console.print("S - Selecionar este diretório")
        console.print("Q - Voltar ao menu principal")
        
        return dirs

    def organize_other_directory(self):
        """Organizes files in another directory."""
        current_path = "/"
        
        while True:
            self.clear_screen()
            dirs = self.show_directory_navigation(current_path)
            
            choice = input("\nEscolha uma opção (número do diretório, S para selecionar, Q para sair): ").strip().upper()
            
            if choice == 'Q':
                return
            
            if choice == 'S':
                try:
                    console.print(f"\n[bold]Organizando arquivos em:[/bold] {current_path}")
                    self.execution.organize_all(current_path)
                    console.print("[green]Arquivos organizados com sucesso![/green]")
                except Exception as e:
                    error_msg = f"Erro: {str(e)}"
                    console.print(f"[red]{error_msg}[/red]")
                    self.logger.error(error_msg)
                input("\nPressione Enter para continuar...")
                return
            
            try:
                if choice == 'B':
                    # Voltar ao diretório anterior
                    parent = os.path.dirname(current_path)
                    if os.path.exists(parent):
                        current_path = parent
                    continue
                
                choice_idx = int(choice) - 1
                if 0 <= choice_idx < len(dirs):
                    new_path = os.path.join(current_path, dirs[choice_idx])
                    if os.path.exists(new_path):
                        current_path = new_path
                else:
                    console.print("[red]Opção inválida![/red]")
                    input("\nPressione Enter para continuar...")
            except ValueError:
                console.print("[red]Opção inválida![/red]")
                input("\nPressione Enter para continuar...")

    def show_logs(self):
        """Shows operation logs."""
        try:
            with open('app.log', 'r') as f:
                log_content = f.read()
            
            if not log_content:
                console.print("[yellow]Log file is empty.[/yellow]")
                input("\nPress Enter to return to main menu...")
                return
            else:
                console.print(Panel.fit(
                    "[bold blue]Log file contents:[/bold blue]",
                    title="Logs",
                    border_style="blue"
                ))
                console.print(log_content)
                
                console.print("\n[bold]Options:[/bold]")
                console.print("1. Clear logs")
                console.print("2. Revert last operation")
                console.print("3. Select logs to revert")
                console.print("4. Return to main menu")
                
                while True:
                    choice = input("\nChoose an option [1/2/3/4]: ")
                    if choice == '1':
                        self.clear_logs()
                        return
                    elif choice == '2':
                        self.revert_last_operation()
                        return
                    elif choice == '3':
                        self.select_logs_to_revert()
                        return
                    elif choice == '4':
                        return
                    else:
                        console.print("[red]Invalid option. Please choose between 1 and 4.[/red]")
            
        except FileNotFoundError:
            console.print("[yellow]No logs found[/yellow]")
            input("\nPress Enter to return to main menu...")

    def clear_logs(self):
        """Clears the log file."""
        try:
            with open('app.log', 'w') as f:
                f.write('')
            console.print("[green]Logs cleared successfully![/green]")
        except Exception as e:
            error_msg = f"Error clearing logs: {str(e)}"
            console.print(f"[red]{error_msg}[/red]")
            self.logger.error(error_msg)
        input("\nPress Enter to continue...")

    def revert_last_operation(self):
        """Reverts all file movements from the last operation based on timestamp."""
        try:
            with open('app.log', 'r') as f:
                logs = f.readlines()
            
            if not logs:
                console.print("[yellow]No operations to revert[/yellow]")
                input("\nPress Enter to continue...")
                return
            
            # Filtra apenas os logs de movimentação de arquivos
            move_logs = [log for log in logs if 'movido para a pasta' in log]
            
            if not move_logs:
                console.print("[yellow]No file movement operations found in logs[/yellow]")
                input("\nPress Enter to continue...")
                return
            
            # Obtém o timestamp da última operação
            last_timestamp = None
            last_operation_logs = []
            
            for log in reversed(move_logs):
                # Extrai o timestamp do log (formato: "YYYY-MM-DD HH:MM:SS")
                timestamp = log.split(' - ')[0]
                
                if last_timestamp is None:
                    last_timestamp = timestamp
                    last_operation_logs.append(log)
                elif timestamp == last_timestamp:
                    last_operation_logs.append(log)
                else:
                    break
            
            if not last_operation_logs:
                console.print("[yellow]No operations found to revert[/yellow]")
                input("\nPress Enter to continue...")
                return
            
            # Reverte todos os logs da última operação
            for log in last_operation_logs:
                try:
                    parts = log.split('"')
                    if len(parts) >= 5:
                        filename = parts[1]
                        destination = parts[3]
                        
                        # Obtém o diretório de origem
                        origin = os.path.dirname(destination)
                        
                        # Move o arquivo de volta
                        source_path = os.path.join(destination, filename)
                        target_path = os.path.join(origin, filename)
                        
                        if os.path.exists(source_path):
                            shutil.move(source_path, target_path)
                            self.logger.info(f'Arquivo "{filename}" revertido para "{origin}".')
                            console.print(f"[green]Arquivo {filename} revertido com sucesso![/green]")
                        else:
                            console.print(f"[yellow]Arquivo {filename} não encontrado em {destination}[/yellow]")
                    else:
                        console.print("[yellow]Formato de log inválido para reversão[/yellow]")
                except Exception as e:
                    console.print(f"[red]Erro ao reverter operação: {str(e)}[/red]")
                    self.logger.error(f'Erro ao reverter operação: {str(e)}')
            
            console.print(f"\n[green]Todas as operações de {last_timestamp} foram revertidas com sucesso![/green]")
            
        except Exception as e:
            console.print(f"[red]Erro ao ler logs: {str(e)}[/red]")
            self.logger.error(f'Erro ao ler logs: {str(e)}')
        
        input("\nPress Enter to continue...")

    def select_logs_to_revert(self):
        """Allows user to select specific logs to revert."""
        try:
            with open('app.log', 'r') as f:
                logs = f.readlines()
            
            if not logs:
                console.print("[yellow]No operations to revert[/yellow]")
                input("\nPress Enter to continue...")
                return
            
            # Filtra apenas os logs de movimentação de arquivos
            move_logs = [log for log in logs if 'movido para a pasta' in log]
            
            if not move_logs:
                console.print("[yellow]No file movement operations found in logs[/yellow]")
                input("\nPress Enter to continue...")
                return
            
            # Mostra os logs numerados
            console.print("\n[bold]Select logs to revert (comma-separated numbers) or 'c' to cancel:[/bold]")
            for i, log in enumerate(move_logs, 1):
                parts = log.split('"')
                if len(parts) >= 5:
                    filename = parts[1]
                    destination = parts[3]
                    console.print(f"{i}. {filename} -> {destination}")
            
            # Obtém a seleção do usuário
            while True:
                try:
                    selection = input("\nEnter log numbers to revert (e.g., 1,3,5) or 'c' to cancel: ")
                    if selection.strip().lower() == 'c':
                        console.print("[yellow]Operation cancelled[/yellow]")
                        return
                    
                    if not selection.strip():
                        console.print("[yellow]No logs selected[/yellow]")
                        input("\nPress Enter to continue...")
                        return
                    
                    # Converte a seleção em índices
                    selected_indices = [int(x.strip()) - 1 for x in selection.split(',')]
                    
                    # Verifica se os índices são válidos
                    if any(i < 0 or i >= len(move_logs) for i in selected_indices):
                        console.print("[red]Invalid log numbers[/red]")
                        continue
                    
                    # Reverte os logs selecionados
                    for i in selected_indices:
                        log = move_logs[i]
                        try:
                            parts = log.split('"')
                            if len(parts) >= 5:
                                filename = parts[1]
                                destination = parts[3]
                                
                                # Obtém o diretório de origem
                                origin = os.path.dirname(destination)
                                
                                # Move o arquivo de volta
                                source_path = os.path.join(destination, filename)
                                target_path = os.path.join(origin, filename)
                                
                                if os.path.exists(source_path):
                                    shutil.move(source_path, target_path)
                                    self.logger.info(f'Arquivo "{filename}" revertido para "{origin}".')
                                    console.print(f"[green]Arquivo {filename} revertido com sucesso![/green]")
                                else:
                                    console.print(f"[yellow]Arquivo {filename} não encontrado em {destination}[/yellow]")
                            else:
                                console.print("[yellow]Formato de log inválido para reversão[/yellow]")
                        except Exception as e:
                            console.print(f"[red]Erro ao reverter operação: {str(e)}[/red]")
                            self.logger.error(f'Erro ao reverter operação: {str(e)}')
                    
                    console.print("\n[green]Operações selecionadas revertidas com sucesso![/green]")
                    break
                    
                except ValueError:
                    console.print("[red]Invalid input. Please enter numbers separated by commas or 'c' to cancel[/red]")
                    continue
            
        except Exception as e:
            console.print(f"[red]Erro ao ler logs: {str(e)}[/red]")
            self.logger.error(f'Erro ao ler logs: {str(e)}')
        
        input("\nPress Enter to continue...")

    def start(self):
        """Starts the terminal interface."""
        while True:
            self.clear_screen()
            self.display_header()
            self.display_menu()
            
            choice = self.get_user_choice()
            
            if choice == '1':
                self.organize_current_directory()
            elif choice == '2':
                self.organize_other_directory()
            elif choice == '3':
                self.clear_screen()
                self.display_categories()
                input("\nPress Enter to continue...")
            elif choice == '4':
                self.clear_screen()
                self.show_logs()
            elif choice == '5':
                console.print("\n[green]Thank you for using File Organizer![/green]")
                sys.exit(0) 