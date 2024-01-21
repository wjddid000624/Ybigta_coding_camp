from .base_command import BaseCommand
import os
import shutil
from typing import List

class CopyCommand(BaseCommand):
    def __init__(self, options: List[str], args: List[str]) -> None:
        """
        Initialize the CopyCommand object.

        Args:
            options (List[str]): List of command options.
            args (List[str]): List of command arguments.
        """
        super().__init__(options, args)

        # Override the attributes inherited from BaseCommand
        self.description = 'Copy a file or directory to another location'
        self.usage = 'Usage: cp [source] [destination]'

        # TODO 6-1: Initialize any additional attributes you may need.
        # Refer to list_command.py, grep_command.py to implement this.
        # ...
        if len(args) < 2:
            print('cp: missing file/directory location(s)')
        else:
            self.source = args[0]
            self.destination = args[1]
            self.options = options

    def execute(self) -> None:
        """
        Execute the copy command.
        Supported options:
            -i: Prompt the user before overwriting an existing file.
            -v: Enable verbose mode (print detailed information)
        
        TODO 6-2: Implement the functionality to copy a file or directory to another location.
        You may need to handle exceptions and print relevant error messages.
        You may use the file_exists() method to check if the destination file already exists.
        """
        # Your code here
        if not self.source or not self.destination:
            print('cp: missing file/directory location(s)')
            return
        
        dest_dir = os.path.join(BaseCommand.current_path, self.destination)
        src_dir = os.path.join(BaseCommand.current_path, self.source)

        if '-v' in self.options:
            print(f'cp: copying {src_dir} to {dest_dir}')
        
        file_name = src_dir.split('\\')[-1]
        if self.file_exists(dest_dir, file_name):
            if '-i' in self.options:
                response = input(f'cp: overwrite {dest_dir}? (y/n) ')
                if response.lower() != 'y':
                    print(f"cp: cannot copy '{src_dir}' to '{dest_dir}':  Destination path '{dest_dir}\{file_name}' already exists")
                    return
        
        try:
            shutil.copy(src_dir, dest_dir)
        except Exception as e:
            print(f"cp: {e}")

    def file_exists(self, directory: str, file_name: str) -> bool:
        """
        Check if a file exists in a directory.
        Feel free to use this method in your execute() method.

        Args:
            directory (str): The directory to check.
            file_name (str): The name of the file.

        Returns:
            bool: True if the file exists, False otherwise.
        """
        file_path = os.path.join(directory, file_name)
        return os.path.exists(file_path)
