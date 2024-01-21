# utils/command_parser.py
import logging
from typing import Dict, Any

"""
TODO 10-1: Add a logger object.
Log command name, options, and arguments.

Logging format:
f"Command name: {command_name}"
f"Options: {options}"
f"Positional args: {positional_args}"
"""

class CommandParser:
    """
    A class for parsing commands and extracting command name, options, and arguments.

    Args:
        verbose (bool, optional): If True, print additional information during parsing. Defaults to False.

    Methods:
        parse_command(input_command: str) -> Dict[str, Any]:
            Parses the input command and returns a dictionary containing the command name, options, and arguments.

    """

    def __init__(self, verbose: bool = False) -> None:
        # TODO 2-1: Initialize the verbose attribute.
        self.verbose = verbose
        self.logger = logging.getLogger(__name__)

    def parse_command(self, input_command: str) -> Dict[str, Any]:
        """
        Parses the input command and returns a dictionary containing the command name, options, and positional arguments.

        Args:
            input_command (str): The input command to be parsed.

        Returns:
            dict: A dictionary containing the parsed command information with the following keys:
                - 'command_name': The name of the command.
                - 'options': A list of options specified in the command.
                - 'args': A list of positional arguments specified in the command.
        """

        # TODO 2-2: Remove the following line after implementing the command parsing logic.
        command_name, options, positional_args = '', [], []
        commands = input_command.split()
        command_name = commands[0]
        options = [command for command in commands[1:] if command.startswith('-')]
        positional_args = [command for command in commands[1:] if not command.startswith('-')]

        # If verbose is True, print the parsed command information.
        if self.verbose:
            print(f"Command name: {command_name}")
            print(f"Options: {options}")
            print(f"Positional args: {positional_args}")

        self.logger.info(f"Command name: {command_name}")
        self.logger.info(f"Options: {options}")
        self.logger.info(f"Positional args: {positional_args}")

        return {
            'command_name': command_name,
            'options': options,
            'args': positional_args
        }

