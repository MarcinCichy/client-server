import unittest
from server_package.menu import CommandHandler
from server_package.functions import SystemUtilities
import server_package.server_response as server_response


class TestMenu(unittest.TestCase):
    def setUp(self):
        self.system_utilities = SystemUtilities()

    def test_help_command_with_user_permissions(self):
        user_data = {'marcin': {'login': [{'username': 'marcin'}, {'password': '12345'}]}}
        user_command_handler = CommandHandler()
        user_command_handler.user_data = user_data
        self.assertIn("uptime", user_command_handler.use_command({"username": "help"}))

    def test_help_command_with_admin_permissions(self):
        admin_data = {'permissions': "admin"}
        user_command_handler = CommandHandler()
        user_command_handler.user_data = admin_data
        self.assertIn("user-add", user_command_handler.use_command({'admin_user': 'help'}))

    def test_help_command_with_unknown_permissions(self):
        unknown_data = {'marcin': {'login': [{'username': 'marcin'}, {'password': '12345'}]}}
        user_command_handler = CommandHandler()
        user_command_handler.user_data = unknown_data
        self.assertEqual(user_command_handler.use_command({'unknownusername': 'help'}), server_response.E_WRONG_PERMISSIONS)

    def test_stop_command_with_user_permissions(self):
        user_data = {'marcin': {'login': [{'username': 'marcin'}, {'password': '12345'}]}}
        user_command_handler = CommandHandler()
        user_command_handler.user_data = user_data
        self.assertEqual(user_command_handler.use_command({"username": "stop"}), server_response.E_COMMAND_UNAVAILABLE)

    def test_stop_command_with_admin_permissions(self):
        admin_data = {'marcin': {'login': [{'username': 'marcin'}, {'password': '12345'},{'permissions': 'admin'}]}}
        user_command_handler = CommandHandler()
        user_command_handler.user_data = admin_data
        self.assertEqual(user_command_handler.use_command({'admin_user': 'stop'}), {'Connection': 'close'})

    def test_stop_command_with_unknown_permissions(self):
        # unknown_data = ServerUserState('unknownusername', 'unknown')
        unknown_data = {'marcin': {'login': [{'username': 'marcin'}, {'password': '12345'}]}}
        user_command_handler = CommandHandler()
        user_command_handler.user_data = unknown_data
        self.assertEqual(user_command_handler.use_command({'unknownusername': 'stop'}), server_response.E_COMMAND_UNAVAILABLE)


if __name__ == "__main__":
    unittest.main(verbosity=2)

