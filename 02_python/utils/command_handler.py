# utils/command_handler.py
from commands.list_command import ListCommand
from commands.move_command import MoveCommand
from commands.copy_command import CopyCommand
from commands.change_directory_command import ChangeDirectoryCommand
from commands.print_working_directory_command import PrintWorkingDirectoryCommand
from commands.grep_command import GrepCommand
from utils.command_parser import CommandParser

class CommandHandler:
    """
    A class that handles the execution of commands based on user input.

    Attributes:
        parser (CommandParser): The command parser object used to parse user input.
        commands (dict): A dictionary mapping command names to their corresponding command classes.

    Methods:
        execute(command: str) -> None: Executes the given command by parsing it, creating the corresponding command object,
                                       and executing the command.
    """

    def __init__(self, parser: CommandParser):
        self.parser = parser
        self.commands = {
            'ls': ListCommand,
            'mv': MoveCommand,
            'cp': CopyCommand,
            'cd': ChangeDirectoryCommand,
            'pwd': PrintWorkingDirectoryCommand,
            'grep': GrepCommand
        }

    def execute(self, command: str) -> None:
        """
        Executes the given command by parsing it, creating the corresponding command object,
        and executing the command.

        Args:
            command (str): The command to be executed.

        Raises:
            AssertionError: If the command name is not a string.

        """
        parsed_result = self.parser.parse_command(command)
        command_name = parsed_result['command_name']
        options = parsed_result['options']
        args = parsed_result['args']

        assert type(command_name) == str, "Command name must be a string."

        command_class = self.commands.get(command_name)
        if command_class:
            command = command_class(options, args)

            if options and '-H' in options:
                command.show_usage()
            else:
                command.execute()
        else:
            print(f"Command '{command_name}' not recognized.")
