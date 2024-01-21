# commands/list_command.py
from .base_command import BaseCommand
import os
import time
from typing import List

# TODO 4-1: Debug and fix the AttributeError
# TODO 4-2: Fix the bug of ls -l -t -h now showing the file in order of modified time.
# TODO 4-3: Fix the bug of ls (when no options are specified)
class ListCommand(BaseCommand):
    """
    Represents a command to list the contents of the current directory or specified path.
    """

    def __init__(self, options: List[str], args: List[str]) -> None:
        super().__init__(options, args)

        # Override the attributes inherited from BaseCommand
        self.description = 'List the contents of the current directory or specified path'
        self.usage = 'Usage: ls [path]'

        # Command-specific attributes go here
        self.name = 'ls'
        self.options = options
        self.target_path = self.args[0] if self.args else self.current_path

    def execute(self) -> None:
        """
        Executes the list command based on the provided options and arguments.
        Supported options:
            -l: Display files in long format
            -h: Display file sizes in human-readable format
            -t: Sort files by modified time
        """
        # Handle options like -l, -a, etc.
        # List the current directory or specified path
        human_readable = '-h' in self.options
        sort_by_modified_time = '-t' in self.options
        if '-l' in self.options:
            self._list_files_detailed(self.target_path, human_readable, sort_by_modified_time)
        else:
            self._list_files(self.target_path)

    def _list_files(self, dir_path: str) -> None:
        """
        Lists the files in the specified directory.

        Args:
            dir_path (str): The path of the directory to list files from.
        """
        with os.scandir(dir_path) as it:
            for entry in it:
                print(entry.name)

    def _list_files_detailed(self, dir_path: str, human_readable: bool = False,
                             sort_by_modified_time: bool = False) -> None:
        """
        Lists the files in the specified directory with detailed information.

        Args:
            dir_path (str): The path of the directory to list files from.
            human_readable (bool, optional): Whether to display file sizes in human-readable format. Defaults to False.
            sort_by_modified_time (bool, optional): Whether to sort files by modified time. Defaults to False.
        """
        files = []
        with os.scandir(dir_path) as it:
            for entry in it:
                name = entry.name
                stats = entry.stat()
                last_modified = time.ctime(stats.st_mtime)
                size = self.human_readable_size(stats.st_size) if human_readable else stats.st_size
                files.append((name, last_modified, size))

        if sort_by_modified_time:
            # Sort by modified time
            files.sort(key=lambda x: x[1], reverse=True)

        for name, last_modified, size in files:
            print(f"{name:20} {last_modified:20} {size:10}")

    def human_readable_size(self, size: int, decimal_places: int = 2) -> str:
        """
        Converts the given size in bytes to a human-readable format.

        Args:
            size (int): The size in bytes.
            decimal_places (int, optional): The number of decimal places to round the size. Defaults to 2.

        Returns:
            str: The human-readable size.
        """
        for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
            if size < 1024.0:
                break
            size /= 1024.0
        return f"{size:.{decimal_places}f} {unit}"