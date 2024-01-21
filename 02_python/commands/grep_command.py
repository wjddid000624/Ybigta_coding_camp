import re
from typing import List
from .base_command import BaseCommand

"""
TODO 9-1: Fix the bug of grep not printing the matched line.

Use breakpoint() and following commands to debug:
- list (l): list the code around the current breakpoint
- continue (c): continue execution until the next breakpoint
- next (n): execute the next line of code
- step (s): execute the next line of code, stepping into function calls
- quit (q): quit the debugger and the program
- help (h): show the help message
"""

class GrepCommand(BaseCommand):
    def __init__(self, options: List[str], args: List[str]) -> None:
        """
        Initialize the GrepCommand object.

        Args:
            options (List[str]): List of command options.
            args (List[str]): List of command arguments (pattern and file name).
        """
        super().__init__(options, args)

        # Override the attributes inherited from BaseCommand
        self.description = 'Search for a pattern in a file'
        self.usage = 'Usage: grep [OPTION]... PATTERN FILE'
        
        # Command-specific attributes go here
        self.name = 'grep'
        self.pattern = args[0] if args else ''
        self.file = args[1] if len(args) > 1 else ''
        self.options = options

    def execute(self) -> None:
        """
        Execute the grep command.
        Supported options:
            -n: Prefix each line of output with the line number within its input file.
        """
        # Compile the pattern
        pattern = re.compile(self.pattern)

        # Process the file
        try:
            with open(self.file, 'r') as file:
                for line_number, line in enumerate(file, start=1):
                    if pattern.search(line):
                        self.print_line(line_number, line, '-n' in self.options)
                    result = pattern.search(line)
                    print(result)
                        
        except FileNotFoundError:
            print(f"grep: {self.file}: No such file or directory")

    def print_line(self, line_number, line, show_line_number):
        """
        Print the matched line with or without the line number.
        """
        if show_line_number:
            print(f"{line_number}:{line.strip()}")
        else:
            print(line.strip())
