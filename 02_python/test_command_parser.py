import unittest
from utils.command_parser import CommandParser

class TestCommandParser(unittest.TestCase):

    def setUp(self):
        self.parser = CommandParser(verbose=False)

    def test_parse_command_basic(self):
        input_command = "ls -l /home"
        expected_result = {
            'command_name': 'ls',
            'options': ['-l'],
            'args': ['/home']
        }
        result = self.parser.parse_command(input_command)
        self.assertEqual(result, expected_result)

    def test_parse_command_no_options(self):
        input_command = "pwd"
        expected_result = {
            'command_name': 'pwd',
            'options': [],
            'args': []
        }
        result = self.parser.parse_command(input_command)
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
