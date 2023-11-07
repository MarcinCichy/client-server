import unittest
# from unittest.mock import patch
import server_package.server_response as server_response
from server_package.menu import CommandHandler
from server_package.server_user_state import ServerUserState


class TestMenu(unittest.TestCase):
    def setUp(self):
        self.logged_in_user_data = ServerUserState()
        self.logged_in_user_data.logged_in_username = 'username'
        self.logged_in_user_data.logged_in_permissions = 'user'
        self.command_handler = CommandHandler(self.logged_in_user_data)

    def test_use_command_with_valid_user_command(self):
        entrance_command = {'username': 'help'}
        expected_result = server_response.USER_HELP_DICT
        expected_result_with_additional_info = {'line1': 'line', 'Commands for All': ''}
        expected_result_with_additional_info.update(expected_result)

        self.command_handler.sys_utils.help.return_value = expected_result_with_additional_info

        result = self.command_handler.use_command(entrance_command)

        self.assertEqual(result, expected_result_with_additional_info)

        # self.command_handler.sys_utils.help.assert_called_with('user', 'basic')
        # self.command_handler.sys_utils.help.assert_called()


    if __name__ == "__main__":
        unittest.main(verbosity=2)