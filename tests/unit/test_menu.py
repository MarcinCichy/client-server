import unittest
from unittest.mock import MagicMock
from server_package.menu import CommandHandler
import server_package.server_response as server_response


class TestCommandHandler(unittest.TestCase):
    def setUp(self):
        self.mock_database_support = MagicMock()
        self.mock_logged_in_user_data = MagicMock()
        self.command_handler = CommandHandler(logged_in_user_data=self.mock_logged_in_user_data)

        self.command_handler.user_auth.login = MagicMock()
        self.command_handler.sys_utils.help = MagicMock()

        self.mock_logged_in_user_data.logged_in_permissions = 'user'

    def test_use_command_with_valid_user_command(self):
        entrance_command = {'username': {'help': None}}
        expected_result = {
            "line1": "line",
            "Commands for All": ""
        }
        server_response.USER_HELP_DICT

        self.command_handler.sys_utils.help.return_value = expected_result

        result = self.command_handler.use_command(entrance_command)

        self.assertEqual(result, expected_result)
        self.command_handler.sys_utils.help.assert_called_once_with('user')


if __name__ == '__main__':
    unittest.main()