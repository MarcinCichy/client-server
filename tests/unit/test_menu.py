import unittest
from server_package.menu import CommandHandler
from server_package.functions import SystemUtilities
from server_package.server_user_state import ServerUserState
import server_package.server_response as server_response


class TestMenu(unittest.TestCase):
    def setUp(self):
        self.system_utilities = SystemUtilities()

    def test_help_command_with_user_permissions(self):
        user_data = ServerUserState('username', 'user')
        user_command_handler = CommandHandler(user_data)
        self.assertIn("uptime", user_command_handler.use_command({"username": "help"}))

    def test_help_command_with_admin_permissions(self):
        admin_data = ServerUserState('admin_user', 'admin')
        user_command_handler = CommandHandler(admin_data)
        self.assertIn("user-add", user_command_handler.use_command({'admin_user': 'help'}))

    def test_help_command_with_unknown_permissions(self):
        unknown_data = ServerUserState('unknownusername', 'unknown')
        user_command_handler = CommandHandler(unknown_data)
        self.assertEqual(user_command_handler.use_command({'unknownusername': 'help'}), server_response.E_WRONG_PERMISSIONS)








#     @patch('server_package.menu.SystemUtilities')
#     def test_admin_commands_stop_with_different_user_permissions(self, mock_sys_utils):
#         expected_stop_output_admin = {'Connection': 'close'}
#         expected_stop_output_user = {"Error": "Command unavailable. No permissions"}
#         expected_stop_output_unknown = {"Error": "Command unavailable. No permissions"}
#         mock_sys_utils.return_value.stop.return_value = expected_stop_output_admin
#
#         admin_data = ServerUserState()
#         admin_data.logged_in_username = 'adminusername'
#         admin_data.logged_in_permissions = 'admin'
#         admin_command_handler = CommandHandler(admin_data)
#
#         admin_result = admin_command_handler.use_command({'command': 'stop'})
#         self.assertEqual(admin_result, expected_stop_output_admin)
#
#         user_data = ServerUserState()
#         user_data.logged_in_username = 'username'
#         user_data.logged_in_permissions = 'user'
#         user_command_handler = CommandHandler(user_data)
#
#         user_result = user_command_handler.use_command({'command': 'stop'})
#         self.assertEqual(user_result, expected_stop_output_user)
#
#         unknown_data = ServerUserState()
#         unknown_data.logged_in_username = 'username'
#         unknown_data.logged_in_permissions = 'unknown'
#         unknown_command_handler = CommandHandler(unknown_data)
#
#         unknown_result = unknown_command_handler.use_command({'command': 'stop'})
#         self.assertEqual(unknown_result, expected_stop_output_unknown)


if __name__ == "__main__":
    unittest.main(verbosity=2)
