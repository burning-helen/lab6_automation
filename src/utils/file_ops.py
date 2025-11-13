import os
import shutil

class FileOperations:
    def __init__(self, master):
        self.master = master

    def _validate_path(self, path):
        abs_path = os.path.abspath(os.path.join(self.master.curr_dir, path))
        if not abs_path.startswith(self.master.work_dir):
            raise ValueError("Access denied: cannot operate outside working directory")

    def create_file(self, filename):
        """Create an empty file"""
        self._validate_path(filename)
        with open(os.path.join(self.master.curr_dir, filename), 'w'):
            pass
        print(f"File '{filename}' created")

    def read_file(self, filename):
        """Read file content"""
        self._validate_path(filename)
        with open(os.path.join(self.master.curr_dir, filename), 'r') as f:
            print(f.read())

    def write_file(self, filename, *text):
        """Write text to file (overwrites existing content)"""
        self._validate_path(filename)
        text = ' '.join(text)
        with open(os.path.join(self.master.curr_dir, filename), 'w') as f:
            f.write(text)
        print(f"Text written to '{filename}'")

    def remove_file(self, filename):
        """Remove file"""
        self._validate_path(filename)
        os.remove(os.path.join(self.master.curr_dir, filename))
        print(f"File '{filename}' removed")

    def copy_file(self, src, dest):
        """Copy file"""
        self._validate_path(src)
        self._validate_path(dest)
        shutil.copy2(
            os.path.join(self.master.curr_dir, src),
            os.path.join(self.master.curr_dir, dest)
        )
        print(f"File '{src}' copied to '{dest}'")

    def move_file(self, src, dest):
        """Move file"""
        self._validate_path(src)
        self._validate_path(dest)
        shutil.move(
            os.path.join(self.master.curr_dir, src),
            os.path.join(self.master.curr_dir, dest)
        )
        print(f"File '{src}' moved to '{dest}'")

    def rename_file(self, old_name, new_name):
        """Rename file"""
        self.move_file(old_name, new_name)