import unittest
import os
from io import StringIO
import sys
from commands.print_working_directory_command import PrintWorkingDirectoryCommand

class TestPrintWorkingDirectoryCommand(unittest.TestCase):

    def setUp(self):
        self.held, sys.stdout = sys.stdout, StringIO()

    def test_pwd_command(self):
        # Run the command
        command = PrintWorkingDirectoryCommand(options=[], args=[])
        command.execute()

        # Check the output
        output = sys.stdout.getvalue().strip()
        expected_output = os.getcwd()
        self.assertEqual(output, expected_output)

    def tearDown(self):
        sys.stdout = self.held

if __name__ == '__main__':
    unittest.main()
