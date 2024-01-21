import unittest
import os
from commands.change_directory_command import ChangeDirectoryCommand

class TestChangeDirectoryCommand(unittest.TestCase):

    def setUp(self):
        # Store the original working directory
        self.original_directory = os.getcwd()

    def test_change_directory(self):
        # Create a temporary directory
        temp_dir = os.path.dirname(__file__)
        
        # Run the command
        command = ChangeDirectoryCommand(options=[], args=[temp_dir])
        command.execute()

        # Check the output
        self.assertEqual(os.getcwd(), temp_dir)


        temp_dir2 = os.path.join(temp_dir, "tests")
        command = ChangeDirectoryCommand(options=[], args=[temp_dir2])
        command.execute()

        # Check the output
        self.assertEqual(os.getcwd(), temp_dir2)
    

    def tearDown(self):
        # Restore the original working directory
        os.chdir(self.original_directory)

if __name__ == '__main__':
    unittest.main()
