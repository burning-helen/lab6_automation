"""
File Manager Package

This package provides a command-line file manager with the following modules:
- file_ops: File operations (create, read, write, delete, copy, move, rename)
- dir_ops: Directory operations (create, remove)
- navigation: Filesystem navigation (list directory, change directory)
- main: Main application logic and user interface
"""

__version__ = "1.0.0"

from .file_ops import FileOperations
from .dir_ops import DirectoryOperations
from .navigation import Navigation
from .configreader import ConfigReader

__all__ = ['FileOperations', 'DirectoryOperations', 'Navigation', 'ConfigReader']

print(f"Initializing File Manager {__version__}")