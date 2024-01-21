import unittest
import os
import shutil
import tempfile
from commands.move_command import MoveCommand

class TestMoveCommand(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory
        self.temp_dir = tempfile.mkdtemp()
        self.source_file = os.path.join(self.temp_dir, "test_file.txt")
        with open(self.source_file, "w") as f:
            f.write("Test content")

        self.dest_dir = tempfile.mkdtemp()

    def test_move_file(self):
        # Execute the move command
        command = MoveCommand(options=[], args=[self.source_file, self.dest_dir])
        command.execute()

        # Check if the file is moved
        moved_file = os.path.join(self.dest_dir, "test_file.txt")
        self.assertTrue(os.path.exists(moved_file))

    def tearDown(self):
        # Remove the temporary directory after the test
        shutil.rmtree(self.temp_dir)
        shutil.rmtree(self.dest_dir)

if __name__ == '__main__':
    unittest.main()
