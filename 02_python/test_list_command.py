import unittest
import os
import tempfile
from commands.list_command import ListCommand
from io import StringIO
import sys

class TestListCommand(unittest.TestCase):

    def setUp(self):
        # Set up the output buffer
        self.held, sys.stdout = sys.stdout, StringIO()

        # Create a temporary directory and files
        self.temp_dir = tempfile.mkdtemp()

        # Create temporary files
        self.temp_file1 = os.path.join(self.temp_dir, "hello.txt")
        self.temp_file2 = os.path.join(self.temp_dir, "qwe.txt")
        with open(self.temp_file1, 'w') as f:
            f.write("Hello World")
        with open(self.temp_file2, 'w') as f:
            f.write("Test file")

    def test_list_files(self):
        # Run the command
        command = ListCommand(options=[], args=[self.temp_dir])
        command.execute()
        output = sys.stdout.getvalue().strip()

        # Check the output
        self.assertIn("hello.txt", output)
        self.assertIn("qwe.txt", output)

    def tearDown(self):
        # Restore the output buffer
        sys.stdout = self.held
        # Remove the temporary files and directory
        os.remove(self.temp_file1)
        os.remove(self.temp_file2)
        os.rmdir(self.temp_dir)

if __name__ == '__main__':
    unittest.main()
