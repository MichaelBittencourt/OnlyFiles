# -*- coding: utf-8 -*-
import logging
import os

class Logger:
    """Class for centralized logging configuration."""

    LOG_FILE = 'app.log'  # Default log file name
    _configured = False  # Internal control for single configuration

    def __init__(self, name=__name__, verbose=False):
        """
        Get a configured logger instance.

        Parameters:
        name (str): Logger name (default: current module name)
        """
        self.logger = logging.getLogger(name)
        self.__verbose = verbose
        
        # Configure logging only on first instantiation
        if not Logger._configured:
            self._setup_logging()
            Logger._configured = True

    def _setup_logging(self):
        handlers_list = []
        if self.__verbose:
            handlers_list = [
                logging.FileHandler(self.LOG_FILE, encoding='utf-8'),
                logging.StreamHandler()
            ]
        else:
            handlers_list = [logging.FileHandler(self.LOG_FILE, encoding='utf-8')]

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            handlers=handlers_list
        )

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
                with open(self.LOG_FILE, 'r', encoding='utf-8') as f:
                    log_content = f.read()
                if log_content:
                    return log_content
                return "No logs found"
            elif action == 'clear':
                with open(self.LOG_FILE, 'w', encoding='utf-8') as f:
                    f.write('')
                return "Logs cleared successfully"
        except FileNotFoundError:
            return "No logs found"
        except Exception as e:
            return f"Failed to {action} logs: {str(e)}"

    def clear_logs(self):
        """Clear all logs with UTF-8 handling"""
        try:
            with open(self.LOG_FILE, 'w', encoding='utf-8') as f:
                f.write('')
            return True
        except Exception as e:
            self.error(f"Error clearing logs: {str(e)}")
            return False