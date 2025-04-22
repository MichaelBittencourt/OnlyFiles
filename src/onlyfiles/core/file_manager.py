# -*- coding: utf-8 -*-
import os
import shutil
from onlyfiles.utils.logger import Logger
from onlyfiles.core.file_types import file_types
from datetime import datetime
import time

class FileManager:

    def __init__(self, logger):
        self.__logger = logger
        self.__types = file_types
        self.__excluded_files = [os.path.basename(Logger.LOG_FILE)]  # Excluir o arquivo de log das operações
        self.__excluded_dirs = []

    def add_excluded_directory(self, directory):
        """Adiciona um diretório à lista de diretórios excluídos das operações de movimentação"""
        if os.path.isdir(directory) and directory not in self.__excluded_dirs:
            self.__excluded_dirs.append(directory)
            return True
        return False

    def add_excluded_file(self, file_name):
        """Adiciona um arquivo à lista de arquivos excluídos das operações de movimentação"""
        if file_name not in self.__excluded_files:
            self.__excluded_files.append(file_name)
            return True
        return False

    def __is_excluded(self, file_path):
        """Verifica se um arquivo ou diretório deve ser excluído das operações"""
        # Verificar se é um dos arquivos excluídos
        if os.path.basename(file_path) in self.__excluded_files:
            return True
        
        # Verificar se está em um diretório excluído
        for excluded_dir in self.__excluded_dirs:
            if os.path.abspath(file_path).startswith(os.path.abspath(excluded_dir)):
                return True
        
        return False

    def list_files(self, origin_path):
        """List files in a directory with UTF-8 encoding"""
        try:
            # UTF-8 handling for path
            origin_path = origin_path.encode('utf-8').decode('utf-8')
            files = os.listdir(origin_path)
            # UTF-8 handling for filenames and filter excluded files
            return [f.encode('utf-8').decode('utf-8') for f in files if not self.__is_excluded(os.path.join(origin_path, f))]
        except Exception as e:
            self.__logger.error(f'Error listing files in {origin_path}: {str(e)}')
            return []

    def __validate_paths(self, origin_path, destination_path):
        """Private method to validate source and destination paths"""
        try:
            # UTF-8 handling for paths
            origin_path = origin_path.encode('utf-8').decode('utf-8')
            destination_path = destination_path.encode('utf-8').decode('utf-8')

            if not os.path.exists(origin_path):
                raise FileNotFoundError(f"Source path does not exist: {origin_path}")
            if not os.path.exists(destination_path):
                os.makedirs(destination_path, exist_ok=True)
            return True
        except Exception as e:
            self.__logger.error(f'Error validating paths: {str(e)}')
            return False

    def __move_file(self, source_path, destination_path, file):
        """Move a single file with UTF-8 handling"""
        try:
            source_file = os.path.join(source_path, file)
            dest_file = os.path.join(destination_path, file)
            
            # Verificar se é um arquivo excluído
            if self.__is_excluded(source_file):
                self.__logger.info(f'Arquivo "{file}" ignorado (na lista de exclusão).')
                return False

            # Tratamento UTF-8 para os caminhos completos
            source_file = source_file.encode('utf-8').decode('utf-8')
            dest_file = dest_file.encode('utf-8').decode('utf-8')

            shutil.move(source_file, dest_file)
            self.__logger.info(f'Arquivo "{file}" movido para a pasta "{destination_path}".')
            return True
        except Exception as e:
            self.__logger.error(f'Error moving file {file}: {str(e)}')
            return False

    def move_files_by_type(self, origin_path, destination_path, extensions_list):
        if not self.__validate_paths(origin_path, destination_path):
            return

        # List all files from source
        files = self.list_files(origin_path)

        if not files:
            print("Source folder is empty!")
            return

        # Get destination folder name to ignore it
        destination_folder_name = os.path.basename(destination_path)

        # Flag to check if found files of the type
        found_files = False

        for file in files:
            # Ignore destination folder if it already exists
            if file == destination_folder_name:
                continue

            path_file = os.path.join(origin_path, file)

            # Check if it's a file
            if os.path.isfile(path_file):
                # Get file extension
                for ext in extensions_list:
                    if file.endswith(ext):
                        # Create folder only if found the first file of the type
                        if not found_files:
                            os.makedirs(destination_path, exist_ok=True)
                            found_files = True

                        self.__move_file(path_file, destination_path, file)
                        break
            else:
                print(f'"{file}" is not a file, ignoring.')

    def move_other_files(self, origin_path, destination_path, types_dict):
        """Move files that don't fit into any category to the Others folder"""
        if not self.__validate_paths(origin_path, destination_path):
            return

        # List all files from source
        files = self.list_files(origin_path)

        if not files:
            print("Source folder is empty!")
            return

        # Get destination folder name to ignore it
        destination_folder_name = os.path.basename(destination_path)

        # Get all known extensions from types_dict
        known_extensions = set()
        for ext_list in types_dict.values():
            known_extensions.update(ext.lower() for ext in ext_list)

        # Flag to check if found files of the type
        found_files = False

        for file in files:
            # Ignore destination folder if it already exists
            if file == destination_folder_name:
                continue

            path_file = os.path.join(origin_path, file)

            # Check if it's a file
            if os.path.isfile(path_file):
                # Get file extension
                _, ext = os.path.splitext(file)

                # If extension is not in any known category
                if ext.lower() not in known_extensions:
                    # Create folder only if found the first unlisted file
                    if not found_files:
                        os.makedirs(destination_path, exist_ok=True)
                        found_files = True

                    self.__move_file(path_file, destination_path, file)
            else:
                print(f'"{file}" is not a file, ignoring.')

    def organize_by_extension(self, directory):
        """Organize files by their extensions"""
        try:
            # Tratamento UTF-8 para o diretório
            directory = directory.encode('utf-8').decode('utf-8')

            files = os.listdir(directory)
            for file in files:
                file_path = os.path.join(directory, file)
                
                # Ignorar arquivos excluídos e diretórios
                if self.__is_excluded(file_path) or not os.path.isfile(file_path):
                    continue
                    
                ext = os.path.splitext(file)[1].lower()
                if ext:  # Ignore files without extension
                    ext_dir = os.path.join(directory, ext[1:])  # Remove the dot from extension
                    os.makedirs(ext_dir, exist_ok=True)
                    shutil.move(
                        os.path.join(directory, file),
                        os.path.join(ext_dir, file)
                    )
                    self.__logger.info(f"Moved {file} to {ext_dir}")
            return True
        except Exception as e:
            self.__logger.error(f"Error organizing by extension: {str(e)}")
            return False

    def organize_by_date(self, directory):
        """Organize files by their creation date"""
        try:
            # Tratamento UTF-8 para o diretório
            directory = directory.encode('utf-8').decode('utf-8')

            files = os.listdir(directory)
            for file in files:
                file_path = os.path.join(directory, file)
                
                # Ignorar arquivos excluídos e diretórios
                if self.__is_excluded(file_path) or not os.path.isfile(file_path):
                    continue
                    
                creation_time = os.path.getctime(file_path)
                date_str = datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d')
                date_dir = os.path.join(directory, date_str)
                os.makedirs(date_dir, exist_ok=True)
                shutil.move(file_path, os.path.join(date_dir, file))
                self.__logger.info(f"Moved {file} to {date_dir}")
            return True
        except Exception as e:
            self.__logger.error(f"Error organizing by date: {str(e)}")
            return False

    def organize_by_size(self, directory):
        """Organize files by their size"""
        try:
            # Tratamento UTF-8 para o diretório
            directory = directory.encode('utf-8').decode('utf-8')

            files = os.listdir(directory)
            for file in files:
                file_path = os.path.join(directory, file)
                
                # Ignorar arquivos excluídos e diretórios
                if self.__is_excluded(file_path) or not os.path.isfile(file_path):
                    continue
                    
                size_bytes = os.path.getsize(file_path)

                # Convert to appropriate size category
                if size_bytes < 1024:  # Less than 1KB
                    size_dir = "tiny"
                elif size_bytes < 1024 * 1024:  # Less than 1MB
                    size_dir = "small"
                elif size_bytes < 1024 * 1024 * 10:  # Less than 10MB
                    size_dir = "medium"
                elif size_bytes < 1024 * 1024 * 100:  # Less than 100MB
                    size_dir = "large"
                else:
                    size_dir = "huge"

                size_dir_path = os.path.join(directory, size_dir)
                os.makedirs(size_dir_path, exist_ok=True)
                shutil.move(file_path, os.path.join(size_dir_path, file))
                self.__logger.info(f"Moved {file} to {size_dir_path}")
            return True
        except Exception as e:
            self.__logger.error(f"Error organizing by size: {str(e)}")
            return False

    def create_backup(self, directory):
        """Create a backup of the directory"""
        try:
            # Tratamento UTF-8 para o diretório
            directory = directory.encode('utf-8').decode('utf-8')

            backup_dir = os.path.join(directory, f"backup_{int(time.time())}")
            shutil.copytree(directory, backup_dir, dirs_exist_ok=True)
            self.__logger.info(f"Created backup at {backup_dir}")
            return backup_dir
        except Exception as e:
            self.__logger.error(f"Error creating backup: {str(e)}")
            return None

    def revert_backup(self, directory):
        """Revert to the most recent backup"""
        try:
            # Tratamento UTF-8 para o diretório
            directory = directory.encode('utf-8').decode('utf-8')

            # Find the most recent backup
            backups = [d for d in os.listdir(directory) if d.startswith("backup_")]
            if not backups:
                return False

            latest_backup = max(backups, key=lambda x: int(x.split('_')[1]))
            backup_path = os.path.join(directory, latest_backup)

            # Move files from backup to main directory
            for item in os.listdir(backup_path):
                if item != latest_backup:  # Don't copy the backup folder itself
                    src = os.path.join(backup_path, item)
                    dst = os.path.join(directory, item)
                    if os.path.isdir(src):
                        shutil.copytree(src, dst, dirs_exist_ok=True)
                    else:
                        shutil.copy2(src, dst)

            self.__logger.info(f"Reverted to backup {latest_backup}")
            return True
        except Exception as e:
            self.__logger.error(f"Error reverting backup: {str(e)}")
            return False

    def read_logs(self):
        """Read log file content"""
        try:
            from logger import Logger
            with open(Logger.LOG_FILE, 'r', encoding='utf-8') as f:
                return f.readlines()
        except FileNotFoundError:
            self.__logger.warning(f"Arquivo de log não encontrado em {Logger.LOG_FILE}")
            return []
        except Exception as e:
            self.__logger.error(f"Erro ao ler o arquivo de log: {str(e)}")
            return []

    def get_move_logs(self, logs):
        """Filter file movement logs"""
        # Verificar todos os formatos possíveis de log de movimentação
        move_logs = []
        for log in logs:
            if any(pattern in log for pattern in ['movido para a pasta', 'Arquivo "', 'Moved']):
                move_logs.append(log)
        return move_logs

    def revert_file(self, log):
        """Revert a file based on a log"""
        try:
            # Decodificar o log para lidar com caracteres especiais
            log = log.encode('utf-8').decode('utf-8')
            
            # Detectar o formato da mensagem de log
            if 'Arquivo "' in log and 'movido para a pasta' in log:
                # Formato: 'Arquivo "nome_arquivo" movido para a pasta "caminho_destino".'
                parts = log.split('"')
                if len(parts) >= 5:
                    filename = parts[1]
                    destination = parts[3]
                    
                    # O destino é o diretório completo
                    source_path = os.path.join(destination, filename)
                    
                    # O destino original é o diretório pai
                    # Usamos dirname uma vez para voltar ao diretório original
                    parent_dir = os.path.dirname(destination)
                    target_path = os.path.join(parent_dir, filename)
                    
                    if os.path.exists(source_path):
                        shutil.move(source_path, target_path)
                        self.__logger.info(f'Arquivo "{filename}" revertido para "{parent_dir}".')
                        return True
                    else:
                        self.__logger.warning(f'Arquivo {filename} não encontrado em {destination}')
            elif 'Moved' in log:
                # Formato: 'Moved nome_arquivo to caminho_destino'
                parts = log.split('Moved ')[1].split(' to ')
                if len(parts) == 2:
                    filename = parts[0].strip()
                    destination = parts[1].strip()
                    
                    # O destino é o diretório completo
                    source_path = os.path.join(destination, filename)
                    
                    # O destino original é o diretório pai
                    parent_dir = os.path.dirname(destination)
                    target_path = os.path.join(parent_dir, filename)
                    
                    if os.path.exists(source_path):
                        shutil.move(source_path, target_path)
                        self.__logger.info(f'Arquivo "{filename}" revertido para "{parent_dir}".')
                        return True
                    else:
                        self.__logger.warning(f'Arquivo {filename} não encontrado em {destination}')
            else:
                # Formato não reconhecido
                self.__logger.warning('Formato de log não reconhecido para reversão')
                
        except Exception as e:
            self.__logger.error(f'Erro ao reverter operação: {str(e)}')
        return False