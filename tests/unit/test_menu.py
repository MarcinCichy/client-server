import unittest
from server_package.functions import SystemUtilities
from server_package.menu import CommandHandler
from server_package.server_user_state import ServerUserState


class TestMenu(unittest.TestCase):
    def setUp(self):
        self.logged_in_user_data = ServerUserState()
        self.logged_in_user_data.logged_in_username = 'username'
        self.logged_in_user_data.logged_in_permissions = 'user'
        self.command_handler = CommandHandler(self.logged_in_user_data)

    def test_use_command_with_valid_user_command(self):
        entrance_command = {self.logged_in_user_data.logged_in_username: 'help'}
        expected_result = SystemUtilities.help(self.logged_in_user_data.logged_in_permissions)
        self.command_handler.sys_utils.help.return_value = expected_result

        result = self.command_handler.use_command(entrance_command)

        self.assertEqual(result, expected_result)

        # self.command_handler.sys_utils.help.assert_called_with('user', 'basic')
        # self.command_handler.sys_utils.help.assert_called()


if __name__ == "__main__":
    unittest.main(verbosity=2)
