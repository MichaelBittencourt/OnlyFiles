#!/usr/bin/env python3
"""
OnlyFiles - A powerful file management and backup CLI tool.
"""

import sys
from src.cli.commands import cli
from src.utils.logging import Logger

# Initialize logger
logger = Logger()

if __name__ == '__main__':
    try:
        # Click automatically processes command line arguments
        cli(ctx=None)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user. Exiting...")
        sys.exit(0)
    except Exception as e:
        error_message = f"An unexpected error occurred: {str(e)}"
        print(f"\n[ERROR] {error_message}")
        logger.error(error_message)
        sys.exit(1) 