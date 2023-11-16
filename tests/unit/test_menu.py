import unittest
from unittest.mock import patch
from server_package.menu import CommandHandler
from server_package.server_user_state import ServerUserState
# import server_package.server_response as server_response


class TestMenu(unittest.TestCase):
    @patch('server_package.menu.SystemUtilities')
    def test_help_command_with_different_user_permissions(self, mock_sys_utils):
        help_output_user = "Expected Help Output for User"
        help_output_admin = "Expected Help Output for Admin"
        help_output_unknown = "Expected Help Output for Exception"
        mock_sys_utils.return_value.help.side_effect = lambda perm: help_output_user if perm == 'user' else (help_output_admin if perm == 'admin' else help_output_unknown)

        user_data = ServerUserState()
        user_data.logged_in_username = 'username'
        user_data.logged_in_permissions = 'user'
        user_command_handler = CommandHandler(user_data)

        entrance_command = {'username': 'help'}
        user_result = user_command_handler.use_command(entrance_command)

        mock_sys_utils.return_value.help.assert_called_with('user')
        self.assertEqual(user_result, help_output_user)

        admin_data = ServerUserState()
        admin_data.logged_in_username = 'adminusername'
        admin_data.logged_in_permissions = 'admin'
        admin_command_handler = CommandHandler(admin_data)

        entrance_command = {'adminusername': 'help'}
        admin_result = admin_command_handler.use_command(entrance_command)

        mock_sys_utils.return_value.help.assert_called_with('admin')
        self.assertEqual(admin_result, help_output_admin)

        unknown_data = ServerUserState()
        unknown_data.logged_in_username = 'unknownusername'
        unknown_data.logged_in_permissions = 'unknown'
        unknown_command_handler = CommandHandler(unknown_data)

        entrance_command = {'unknownusername': 'help'}
        unknown_result = unknown_command_handler.use_command(entrance_command)

        mock_sys_utils.return_value.help.assert_called_with('unknown')
        self.assertEqual(unknown_result, help_output_unknown)

    @patch('server_package.menu.SystemUtilities')
    def test_admin_commands_stop_with_different_user_permissions(self, mock_sys_utils):
        expected_stop_output_admin = {'Connection': 'close'}
        expected_stop_output_user = {"Error": "Command unavailable. No permissions"}
        expected_stop_output_unknown = {"Error": "Command unavailable. No permissions"}
        mock_sys_utils.return_value.stop.return_value = expected_stop_output_admin

        admin_data = ServerUserState()
        admin_data.logged_in_username = 'adminusername'
        admin_data.logged_in_permissions = 'admin'
        admin_command_handler = CommandHandler(admin_data)

        admin_result = admin_command_handler.use_command({'command': 'stop'})
        self.assertEqual(admin_result, expected_stop_output_admin)

        user_data = ServerUserState()
        user_data.logged_in_username = 'username'
        user_data.logged_in_permissions = 'user'
        user_command_handler = CommandHandler(user_data)

        user_result = user_command_handler.use_command({'command': 'stop'})
        self.assertEqual(user_result, expected_stop_output_user)

        unknown_data = ServerUserState()
        unknown_data.logged_in_username = 'username'
        unknown_data.logged_in_permissions = 'unknown'
        unknown_command_handler = CommandHandler(unknown_data)

        unknown_result = unknown_command_handler.use_command({'command': 'stop'})
        self.assertEqual(unknown_result, expected_stop_output_unknown)


if __name__ == "__main__":
    unittest.main(verbosity=2)
