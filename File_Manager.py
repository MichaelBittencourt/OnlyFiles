import os
import shutil
from logger import Logger
from file_types import file_types
from datetime import datetime
import time

class FileManager:

    def __init__(self, logger):
        self.__logger = logger
        self.__types = file_types

    def list_files(self, origin_path):
        return os.listdir(origin_path)

    def __validate_paths(self, origin_path, destination_path):
        """Private method to validate source and destination paths"""
        if not origin_path or not destination_path:
            print("Error: Source or destination path is empty!")
            return False

        if os.path.abspath(origin_path) == os.path.abspath(destination_path):
            print("Error: Destination folder cannot be the same as source folder.")
            return False

        return True

    def __move_file(self, source_path, destination_path, file):
        """Private method to centralize file movement logic"""
        try:
            shutil.move(source_path, os.path.join(destination_path, file))
            self.__logger.info(f'File "{file}" moved to folder "{destination_path}".')
            return True
        except Exception as error:
            self.__logger.error(f'Error moving file "{file}": {error}')
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
            files = os.listdir(directory)
            for file in files:
                if os.path.isfile(os.path.join(directory, file)):
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
            files = os.listdir(directory)
            for file in files:
                if os.path.isfile(os.path.join(directory, file)):
                    file_path = os.path.join(directory, file)
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
            files = os.listdir(directory)
            for file in files:
                if os.path.isfile(os.path.join(directory, file)):
                    file_path = os.path.join(directory, file)
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
            with open('app.log', 'r') as f:
                return f.readlines()
        except FileNotFoundError:
            return []

    def get_move_logs(self, logs):
        """Filter file movement logs"""
        return [log for log in logs if 'moved to folder' in log]

    def revert_file(self, log):
        """Revert a file based on a log"""
        try:
            parts = log.split('"')
            if len(parts) >= 5:
                filename = parts[1]
                destination = parts[3]
                origin = os.path.dirname(destination)

                source_path = os.path.join(destination, filename)
                target_path = os.path.join(origin, filename)

                if os.path.exists(source_path):
                    shutil.move(source_path, target_path)
                    self.__logger.info(f'File "{filename}" reverted to "{origin}".')
                    return True
                else:
                    self.__logger.warning(f'File {filename} not found in {destination}')
            else:
                self.__logger.warning('Invalid log format for reversion')
        except Exception as e:
            self.__logger.error(f'Error reverting operation: {str(e)}')
        return False