import os

import self
from utils import configreader

class Navigation:
    DEFAULT_DIR = configreader.ConfigReader.load_config(self)
    def __init__(self, master):
        self.master = master

    def _validate_path(self, path):
        abs_path = os.path.abspath(os.path.join(self.master.curr_dir, path))
        if not abs_path.startswith(self.master.work_dir):
            raise ValueError("Access denied: cannot navigate outside working directory")

    def list_dir(self):
        """List directory contents"""
        items = os.listdir(self.master.curr_dir)
        for item in items:
            full_path = os.path.join(self.master.curr_dir, item)
            if os.path.isdir(full_path):
                print(f"[DIR]  {item}")
            else:
                print(f"[FILE] {item}")

    def change_dir(self, path=DEFAULT_DIR):
        """Change current directory"""
        self._validate_path(path)
        
        new_dir = os.path.abspath(os.path.join(self.master.curr_dir, path))
        if not os.path.isdir(new_dir):
            raise ValueError(f"'{path}' is not a directory")
        
        self.master.curr_dir = new_dir