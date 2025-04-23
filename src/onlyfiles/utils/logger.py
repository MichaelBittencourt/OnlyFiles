# -*- coding: utf-8 -*-
import logging
import os
import platform
import sys
from os.path import expanduser, join

class Logger:
    """
    Cross-platform logging utility that configures logging to file and console.
    Handles log directory creation and provides access to log paths.
    
    Usage example:
        # Using the centralized logger
        logger = Logger()
        logger.info("Information message")
    """

    # Dictionary to track configured loggers
    _configured_loggers = {}

    # Default log file path
    LOG_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'docs', 'app.log')

    # Define property methods first to ensure they're properly recognized
    @property
    def log_dir(self):
        """
        Get the log directory path.
        Returns the full path to the directory where logs are stored.
        """
        if not hasattr(self, '_log_dir'):
            self._log_dir = os.path.dirname(Logger.LOG_FILE)
        return self._log_dir

    @property
    def log_file(self):
        """
        Get the log file path.
        Returns the full path to the log file.
        """
        return Logger.LOG_FILE

    def __init__(self, name=__name__, verbose=False):
        """
        Get a configured logger instance.

        Parameters:
        name (str): Logger name (default: current module name)
        verbose (bool): Ignored - logs are always shown in console and saved to file
        """
        # Initialize important attributes first
        self._name = name
        self._configured = False
        self.logger = logging.getLogger(name)

        # Initialize log path attributes and verify
        self._log_dir = os.path.dirname(Logger.LOG_FILE)
        self._log_file = Logger.LOG_FILE

        try:
            # Validate access through properties
            try:
                dir_property = self.log_dir
                file_property = self.log_file
            except Exception as e:
                print(f"ERROR: Failed to access properties after initialization: {str(e)}")
            if not os.path.exists(self._log_dir):
                try:
                    os.makedirs(self._log_dir, exist_ok=True)
                    print(f"Created log directory: {self._log_dir}")
                except Exception as e:
                    print(f"WARNING: Failed to create directory {self._log_dir}: {str(e)}")
                    raise

            # Setup the logger
            logger_key = f"{name}"
            if logger_key not in Logger._configured_loggers:
                self._setup_logging()
                Logger._configured_loggers[logger_key] = True
                self._configured = True

        except Exception as e:
            print(f"WARNING: Logger initialization failed: {str(e)}")
            # Fall back to a directory we can write to
            self._log_dir = os.path.expanduser('~')
            self._log_file = os.path.join(self._log_dir, 'onlyfiles_app.log')
            print(f"Using fallback log location: {self._log_file}")

            # Try to create the handler with the fallback location
            try:
                self._setup_logging()
                self._configured = True
            except Exception as setup_error:
                print(f"ERROR: Failed to setup logging with fallback: {str(setup_error)}")
                # Last resort: only console logging
                self._setup_console_only()

    def _get_log_directory(self):
        """
        Returns the appropriate log directory for the current operating system.

        Windows: %APPDATA%\\OnlyFiles\\logs
        Linux/Unix: ~/.local/share/onlyfiles/logs
        """
        app_name = "OnlyFiles"

        if platform.system() == "Windows":
            # On Windows, use the APPDATA environment variable
            appdata = os.environ.get('APPDATA')
            if appdata:
                return os.path.join(appdata, app_name, 'logs')
            else:
                # Fallback if APPDATA is not available
                return os.path.join(expanduser('~'), 'AppData', 'Roaming', app_name, 'logs')
        else:
            # On Unix systems (Linux, macOS), follow the XDG standard
            xdg_data_home = os.environ.get('XDG_DATA_HOME')
            if xdg_data_home:
                base_dir = xdg_data_home
            else:
                base_dir = os.path.join(expanduser('~'), '.local', 'share')

            # Use consistent app name (lowercase)
            return os.path.join(base_dir, 'onlyfiles', 'logs')

    def _setup_console_only(self):
        """Setup console-only logging as a last resort fallback."""
        self.logger.setLevel(logging.INFO)

        # Clear any existing handlers to avoid duplicates
        if self.logger.handlers:
            for handler in self.logger.handlers:
                self.logger.removeHandler(handler)

        # Add console handler
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S')
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

    def debug_info(self):
        """
        Print detailed debug information about this logger instance.
        This helps with diagnosing issues related to logging configuration.
        """
        print(f"\n=== Logger Debug Info ===")
        print(f"Logger name: {self._name}")
        print(f"Verbose mode: {self.__verbose}")
        print(f"Configured: {self._configured}")
        print(f"Log directory: {self._log_dir}")
        print(f"Log file: {self._log_file}")

        # Check if directories and files exist
        if self._log_dir:
            print(f"Log directory exists: {os.path.exists(self._log_dir)}")
        if self._log_file:
            print(f"Log file exists: {os.path.exists(self._log_file)}")
        print(f"\nHandlers:")
        if not self.logger.handlers:
            print("  No handlers configured")
        else:
            for i, handler in enumerate(self.logger.handlers):
                handler_type = type(handler).__name__
                print(f"  Handler {i+1}: {handler_type}")
                if isinstance(handler, logging.FileHandler):
                    print(f"    - File: {handler.baseFilename}")
                    print(f"    - Encoding: {handler.encoding}")
                    print(f"    - Mode: {handler.mode}")
                    try:
                        print(f"    - File exists: {os.path.exists(handler.baseFilename)}")
                        print(f"    - File size: {os.path.getsize(handler.baseFilename)} bytes")
                    except:
                        print("    - Cannot access file information")

    def _setup_logging(self):
        """
        Configure logging to both file and console.
        """
        # Clear any existing handlers
        self.logger.handlers = []

        # Set the logging level
        self.logger.setLevel(logging.DEBUG)

        # Create formatters
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # Create and configure file handler
        file_handler = logging.FileHandler(self._log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(file_formatter)

        # Create and configure console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(file_formatter)

        # Add handlers to logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

        self._configured = True

    def info(self, message):
        """Log message with UTF-8 handling"""
        try:
            if isinstance(message, str):
                message = message.encode('utf-8').decode('utf-8')
            self.logger.info(message)
        except Exception as e:
            self.logger.error(f"Error logging info message: {str(e)}")

    def error(self, message):
        """Log error message with UTF-8 handling"""
        try:
            if isinstance(message, str):
                message = message.encode('utf-8').decode('utf-8')
            self.logger.error(message)
        except Exception as e:
            self.logger.error(f"Error logging error message: {str(e)}")

    def exception(self, message):
        """Log complete error with UTF-8 handling"""
        try:
            if isinstance(message, str):
                message = message.encode('utf-8').decode('utf-8')
            self.logger.exception(message)
        except Exception as e:
            self.logger.error(f"Error logging exception: {str(e)}")

    def warning(self, message):
        """Log warning message with UTF-8 handling"""
        try:
            if isinstance(message, str):
                message = message.encode('utf-8').decode('utf-8')
            self.logger.warning(message)
        except Exception as e:
            self.logger.error(f"Error logging warning message: {str(e)}")

    def handle_logs(self, action: str = 'read'):
        """Handle logs operations with UTF-8 handling"""
        try:
            if action == 'read':
                with open(self._log_file, 'r', encoding='utf-8') as f:
                    log_content = f.read()
                if log_content:
                    return log_content
                return "No logs found"
            elif action == 'clear':
                with open(self._log_file, 'w', encoding='utf-8') as f:
                    f.write('')
                return "Logs cleared successfully"
        except FileNotFoundError:
            return "No logs found"
        except Exception as e:
            return f"Failed to {action} logs: {str(e)}"

    def clear_logs(self):
        """Clear all logs with UTF-8 handling"""
        try:
            with open(self._log_file, 'w', encoding='utf-8') as f:
                f.write('')
            return True
        except Exception as e:
            self.error(f"Error clearing logs: {str(e)}")
            return False