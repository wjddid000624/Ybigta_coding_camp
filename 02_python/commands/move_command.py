from .base_command import BaseCommand
import os
import shutil
from typing import List

class MoveCommand(BaseCommand):
    def __init__(self, options: List[str], args: List[str]) -> None:
        """
        Initialize the MoveCommand object.

        Args:
            options (List[str]): List of command options.
            args (List[str]): List of command arguments.
        """
        super().__init__(options, args)

        # Override the attributes inherited from BaseCommand
        self.description = 'Move a file or directory to another location'
        self.usage = 'Usage: mv [source] [destination]'

        # TODO 5-1: Initialize any additional attributes you may need.
        # Refer to list_command.py, grep_command.py to implement this.
        # ...
        if len(args) < 2:
            print('mv: missing file/directory location(s)')
        else:
            self.source = args[0]
            self.destination = args[1]
            self.options = options


    def execute(self) -> None:
        """
        Execute the move command.
        Supported options:
            -i: Prompt the user before overwriting an existing file.
            -v: Enable verbose mode (print detailed information)
        
        TODO 5-2: Implement the functionality to move a file or directory to another location.
        You may need to handle exceptions and print relevant error messages.
        """
        # Your code here
        if not self.source or not self.destination:
            print('mv: missing file/directory location(s)')
            return
        
        src_dir = os.path.join(BaseCommand.current_path, self.source)
        dest_dir = os.path.join(BaseCommand.current_path, self.destination)

        if '-v' in self.options:
            print(f'mv: moving {src_dir} to {dest_dir}')

        # get file name from src_dir
        file_name = src_dir.split('\\')[-1]
        if self.file_exists(dest_dir, file_name):
            if '-i' in self.options:
                response = input(f'mv: overwrite {dest_dir}? (y/n) ')
                if response.lower() != 'y':
                    print(f"mv: cannot move '{src_dir}' to '{dest_dir}':  Destination path '{dest_dir}\{file_name}' already exists")
                    return
            print(f"mv: cannot move '{src_dir}' to '{dest_dir}':  Destination path '{dest_dir}\{file_name}' already exists")
            return

        try:
            shutil.move(src_dir, dest_dir)
        except Exception as e:
            print(f"Error: {e}")
        


    
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
