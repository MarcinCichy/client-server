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

    def test_stop_command_with_user_permissions(self):
        user_data = ServerUserState('username', 'user')
        user_command_handler = CommandHandler(user_data)
        self.assertEqual(user_command_handler.use_command({"username": "stop"}), server_response.E_COMMAND_UNAVAILABLE)

    def test_stop_command_with_admin_permissions(self):
        admin_data = ServerUserState('admin_user', 'admin')
        user_command_handler = CommandHandler(admin_data)
        self.assertEqual(user_command_handler.use_command({'admin_user': 'stop'}), {'Connection': 'close'})

    def test_stop_command_with_unknown_permissions(self):
        unknown_data = ServerUserState('unknownusername', 'unknown')
        user_command_handler = CommandHandler(unknown_data)
        self.assertEqual(user_command_handler.use_command({'unknownusername': 'stop'}), server_response.E_COMMAND_UNAVAILABLE)


if __name__ == "__main__":
    unittest.main(verbosity=2)

