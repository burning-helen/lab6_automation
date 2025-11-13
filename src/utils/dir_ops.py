import os

class DirectoryOperations:
    def __init__(self, master):
        self.master = master

    def _validate_path(self, path):
        abs_path = os.path.abspath(os.path.join(self.master.work_dir, path))
        if not abs_path.startswith(self.master.work_dir):
            raise ValueError("Access denied: cannot operate outside working directory")

    def create_dir(self, dirname):
        """Create directory"""
        self._validate_path(dirname)
        os.makedirs(os.path.join(self.master.curr_dir, dirname), exist_ok=True)
        print(f"Directory '{dirname}' created")

    def remove_dir(self, dirname):
        """Remove directory (must be empty)"""
        self._validate_path(dirname)
        os.rmdir(os.path.join(self.master.curr_dir, dirname))
        print(f"Directory '{dirname}' removed")