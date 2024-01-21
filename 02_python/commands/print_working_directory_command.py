from .base_command import BaseCommand
import os
from typing import List

class PrintWorkingDirectoryCommand(BaseCommand):
    def __init__(self, options: List[str], args: List[str]) -> None:
        """
        Initialize the PrintWorkingDirectoryCommand object.

        Args:
            options (List[str]): List of command options.
            args (List[str]): List of command arguments.
        """
        super().__init__(options, args)

        # Override the attributes inherited from BaseCommand
        self.description = 'Print the current working directory'
        self.usage = 'Usage: pwd'

        # TODO 8-1: Initialize any additional attributes you may need.
        # Refer to list_command.py, grep_command.py to implement this.
        # ...

    def execute(self) -> None:
        """
        Execute the pwd command.
        Supported options:
            None
        
        TODO 8-2: Implement the functionality to print the current working directory.
        No need to handle exceptions.
        """
        # Your code here
        print(BaseCommand.current_path)
