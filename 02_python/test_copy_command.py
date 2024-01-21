import unittest
import os
import tempfile
import shutil
from unittest.mock import patch
from commands.copy_command import CopyCommand

class TestCopyCommand(unittest.TestCase):

    def setUp(self):
        # Create a temporary file and directory
        self.temp_dir = tempfile.mkdtemp()
        self.source_file = os.path.join(self.temp_dir, "source.txt")
        with open(self.source_file, "w") as f:
            f.write("Test content")

        self.destination_dir = tempfile.mkdtemp()

    def test_copy_file(self):
        # Run the command
        command = CopyCommand(options=[], args=[self.source_file, self.destination_dir])
        command.execute()

        # Check the output
        copied_file = os.path.join(self.destination_dir, "source.txt")
        self.assertTrue(os.path.exists(copied_file))

    @patch('builtins.input', return_value='y')
    def test_copy_file_with_overwrite(self, mock_input):
        # Create a file with the same name in the destination directory
        shutil.copy(self.source_file, self.destination_dir)

        # Run the command with the -i option
        command = CopyCommand(options=['-i'], args=[self.source_file, self.destination_dir])
        command.execute()

        # Check the output
        copied_file = os.path.join(self.destination_dir, "source.txt")
        self.assertTrue(os.path.exists(copied_file))

    def tearDown(self):
        # Remove the temporary file and directory
        shutil.rmtree(self.temp_dir)
        shutil.rmtree(self.destination_dir)

if __name__ == '__main__':
    unittest.main()
