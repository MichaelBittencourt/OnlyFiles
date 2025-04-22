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
        self.__excluded_files = [os.path.basename(Logger.LOG_FILE)]  # Exclude the log file carts operations
        self.__excluded_dirs = []

    def add_excluded_directory(self, directory):
        """Add a directory to the list of directories excluded from move operations"""
        if os.path.isdir(directory) and directory not in self.__excluded_dirs:
            self.__excluded_dirs.append(directory)
            return True
        return False

    def add_excluded_file(self, file_name):
        """Add a file to the list of files excluded from move operations"""
        if file_name not in self.__excluded_files:
            self.__excluded_files.append(file_name)
            return True
        return False

    def __is_excluded(self, file_path):
        """Check if a file or directory should be excluded from operations"""
        # Check if it is one of the excluded files
        if os.path.basename(file_path) in self.__excluded_files:
            return True
        
        # Check if it is in an excluded directory
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
            origin_path = os.path.abspath(origin_path.encode('utf-8').decode('utf-8'))
            destination_path = os.path.abspath(destination_path.encode('utf-8').decode('utf-8'))

            if not os.path.exists(origin_path):
                raise FileNotFoundError(f"Source path does not exist: {origin_path}")
            
            # Create destination directory and all parent directories if they don't exist
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
            
            # Check if it is an excluded file
            if self.__is_excluded(source_file):
                self.__logger.info(f'File "{file}" ignored (in exclusion list).')
                return False

            # Check if the source file exists
            if not os.path.exists(source_file):
                self.__logger.warning(f'File "{file}" not found in {source_path}.')
                return False

            # Check write permissions in the destination
            if not os.access(destination_path, os.W_OK):
                self.__logger.error(f'No write permission in {destination_path}.')
                return False

            # UTF-8 handling for full paths
            source_file = source_file.encode('utf-8').decode('utf-8')
            dest_file = dest_file.encode('utf-8').decode('utf-8')

            shutil.move(source_file, dest_file)
            self.__logger.info(f'File "{file}" moved to folder "{destination_path}".')
            return True
        except PermissionError as e:
            self.__logger.error(f'Permission error moving file {file}: {str(e)}')
            return False
        except OSError as e:
            self.__logger.error(f'System error moving file {file}: {str(e)}')
            return False
        except Exception as e:
            self.__logger.error(f'Error moving file {file}: {str(e)}')
            return False

    def move_files_by_type(self, origin_path, destination_path, extensions_list):
        """Move files of specified types to the destination folder"""
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

                        self.__move_file(origin_path, destination_path, file)
                        break
            else:
                print(f'"{file}" is not a file, ignoring.')

    def move_other_files(self, origin_path, destination_path, types_dict):
        """Move files that don't fit into any category to the Others folder"""
        if not self.__validate_paths(origin_path, destination_path):
            return
        
        # Create the "Others" folder immediately after path validation
        try:
            os.makedirs(destination_path, exist_ok=True)
        except Exception as e:
            self.__logger.error(f'Error creating "Others" folder in {destination_path}: {str(e)}')
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
                    self.__move_file(origin_path, destination_path, file)
            else:
                print(f'"{file}" is not a file, ignoring.')

    def organize_by_extension(self, directory):
        """Organize files by their extensions"""
        try:
            # UTF-8 handling for directory
            directory = directory.encode('utf-8').decode('utf-8')

            files = os.listdir(directory)
            for file in files:
                file_path = os.path.join(directory, file)
                
                # Ignore excluded files and directories
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
            # UTF-8 handling for directory
            directory = directory.encode('utf-8').decode('utf-8')

            files = os.listdir(directory)
            for file in files:
                file_path = os.path.join(directory, file)
                
                # Ignore excluded files and directories
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
            # UTF-8 handling for directory
            directory = directory.encode('utf-8').decode('utf-8')

            files = os.listdir(directory)
            for file in files:
                file_path = os.path.join(directory, file)
                
                # Ignore excluded files and directories
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

    def organize_by_type(self, directory):
        """Organize files by their type (e.g., documents, images, videos, etc.)"""
        try:
            # UTF-8 handling for directory
            directory = directory.encode('utf-8').decode('utf-8')

            files = os.listdir(directory)
            for file in files:
                file_path = os.path.join(directory, file)
                
                # Ignore excluded files and directories
                if self.__is_excluded(file_path) or not os.path.isfile(file_path):
                    continue
                    
                # Get file extension
                _, ext = os.path.splitext(file)
                ext = ext.lower()

                # Determine file type based on extension
                file_type = "others"  # Default type
                for type_name, extensions in self.__types.items():
                    if ext in extensions:
                        file_type = type_name
                        break

                # Create type directory and move file
                type_dir = os.path.join(directory, file_type)
                os.makedirs(type_dir, exist_ok=True)
                shutil.move(file_path, os.path.join(type_dir, file))
                self.__logger.info(f"Moved {file} to {type_dir}")
            return True
        except Exception as e:
            self.__logger.error(f"Error organizing by type: {str(e)}")
            return False

    def create_backup(self, directory):
        """Create a backup of the directory"""
        try:
            # UTF-8 handling for directory
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
            # UTF-8 handling for directory
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
            from onlyfiles.utils.logger import Logger
            with open(Logger.LOG_FILE, 'r', encoding='utf-8') as f:
                return f.readlines()
        except FileNotFoundError:
            self.__logger.warning(f"Log file not found at {Logger.LOG_FILE}")
            return []
        except Exception as e:
            self.__logger.error(f"Error reading log file: {str(e)}")
            return []

    def get_move_logs(self, logs):
        """Filter file movement logs"""
        # Check all possible log formats for file movements
        move_logs = []
        for log in logs:
            if any(pattern in log for pattern in ['moved to folder', 'File "', 'Moved']):
                move_logs.append(log)
        return move_logs

    def revert_file(self, log):
        """Revert a file based on a log"""
        try:
            # Decode log to handle special characters
            log = log.encode('utf-8').decode('utf-8')
            
            # Detect log message format
            if 'File "' in log and 'moved to folder' in log:
                # Format: 'File "filename" moved to folder "destination_path".'
                parts = log.split('"')
                if len(parts) >= 5:
                    filename = parts[1]
                    destination = parts[3]
                    
                    # The destination is the full directory
                    source_path = os.path.join(destination, filename)
                    
                    # The original destination is the parent directory
                    parent_dir = os.path.dirname(destination)
                    target_path = os.path.join(parent_dir, filename)
                    
                    if os.path.exists(source_path):
                        shutil.move(source_path, target_path)
                        self.__logger.info(f'File "{filename}" reverted to "{parent_dir}".')
                        return True
                    else:
                        self.__logger.warning(f'File {filename} not found in {destination}')
            elif 'Moved' in log:
                # Format: 'Moved filename to destination_path'
                parts = log.split('Moved ')[1].split(' to ')
                if len(parts) == 2:
                    filename = parts[0].strip()
                    destination = parts[1].strip()
                    
                    # The destination is the full directory
                    source_path = os.path.join(destination, filename)
                    
                    # The original destination is the parent directory
                    parent_dir = os.path.dirname(destination)
                    target_path = os.path.join(parent_dir, filename)
                    
                    if os.path.exists(source_path):
                        shutil.move(source_path, target_path)
                        self.__logger.info(f'File "{filename}" reverted to "{parent_dir}".')
                        return True
                    else:
                        self.__logger.warning(f'File {filename} not found in {destination}')
            else:
                # Unrecognized log format
                self.__logger.warning('Unrecognized log format for reversion')
                
        except Exception as e:
            self.__logger.error(f'Error reverting operation: {str(e)}')
        return False

    def revert_last_action(self):
        """Revert the last complete file movement action based on logs"""
        try:
            # Read all logs
            logs = self.read_logs()
            if not logs:
                self.__logger.warning("No logs found for reversion.")
                return False

            # Filter move-related logs
            move_logs = self.get_move_logs(logs)
            if not move_logs:
                self.__logger.warning("No move logs found for reversion.")
                return False

            # Reverse logs to process the most recent first
            move_logs.reverse()

            # Group logs by action (assuming logs from the same action are consecutive)
            # We consider logs within a short time window (e.g., 5 seconds) as part of the same action
            last_action_logs = []
            last_timestamp = None
            time_threshold = 5  # Seconds

            for log in move_logs:
                # Extract timestamp from log (format: 'YYYY-MM-DD HH:MM:SS - name - level - message')
                try:
                    timestamp_str = log.split(' - ')[0].strip()
                    timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
                except (IndexError, ValueError):
                    continue  # Skip logs with invalid format

                if last_timestamp is None:
                    last_timestamp = timestamp
                    last_action_logs.append(log)
                elif (last_timestamp - timestamp).total_seconds() <= time_threshold:
                    last_action_logs.append(log)
                else:
                    break  # Found a gap, stop grouping

            if not last_action_logs:
                self.__logger.warning("No valid logs found for the last action.")
                return False

            # Revert each file in the last action in reverse order
            success = True
            for log in reversed(last_action_logs):
                if not self.revert_file(log):
                    success = False
                    self.__logger.error(f"Failed to revert part of the last action: {log}")

            if success:
                self.__logger.info("Successfully reverted the last action.")
            else:
                self.__logger.warning("Last action partially reverted due to errors.")
            return success

        except Exception as e:
            self.__logger.error(f"Error reverting last action: {str(e)}")
            return False