import unittest
import os
import tempfile
from io import StringIO
import sys
from commands.grep_command import GrepCommand

class TestGrepCommand(unittest.TestCase):

    def setUp(self):
        # Create a temporary file and write some text to it
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.write(b"Hello World\n")
        self.temp_file.write(b"Another line\n")
        self.temp_file.write(b"Grep test line\n")
        self.temp_file.close()

        self.held, sys.stdout = sys.stdout, StringIO()

    def test_grep_command(self):
        # Execute the GrepCommand
        command = GrepCommand(options=[], args=["Grep", self.temp_file.name])
        command.execute()

        # Check the output
        output = sys.stdout.getvalue().strip()
        self.assertIn("Grep test line", output)

    def test_grep_command_with_line_number(self):
        # Run the command with the -n option
        command = GrepCommand(options=['-n'], args=["Grep", self.temp_file.name])
        command.execute()

        # Check the output
        output = sys.stdout.getvalue().strip()
        self.assertIn("3:Grep test line", output)

    def tearDown(self):
        sys.stdout = self.held
        os.remove(self.temp_file.name)  # Remove the temporary file

if __name__ == '__main__':
    unittest.main()
