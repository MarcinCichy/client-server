# import unittest
# from server_package.functions import SystemUtilities
# from server_package.menu import CommandHandler
# from server_package.server_user_state import ServerUserState
#
#
# class TestMenu(unittest.TestCase):
#     def setUp(self):
#         self.logged_in_user_data = ServerUserState()
#         self.logged_in_user_data.logged_in_username = 'username'
#         self.logged_in_user_data.logged_in_permissions = 'user'
#         self.command_handler = CommandHandler(self.logged_in_user_data)
#
#     def test_use_command_with_valid_user_command(self):
#         entrance_command = {self.logged_in_user_data.logged_in_username: 'help'}
#         expected_result = SystemUtilities.help(self.logged_in_user_data.logged_in_permissions)
#         self.command_handler.sys_utils.help.return_value = expected_result
#
#         result = self.command_handler.use_command(entrance_command)
#
#         self.assertEqual(result, expected_result)
#
#         # self.command_handler.sys_utils.help.assert_called_with('user', 'basic')
#         # self.command_handler.sys_utils.help.assert_called()
#
#
# if __name__ == "__main__":
#     unittest.main(verbosity=2)
import unittest
from unittest.mock import patch
from server_package.menu import CommandHandler
from server_package.server_user_state import ServerUserState
from server_package.functions import SystemUtilities


class TestMenuUserPermissions(unittest.TestCase):
    def setUp(self):
        self.logged_in_user_data = ServerUserState()
        self.logged_in_user_data.logged_in_username = 'username'
        self.logged_in_user_data.logged_in_permissions = 'user'
        self.command_handler = CommandHandler(self.logged_in_user_data)

    # @patch('server_package.functions.SystemUtilities.help')
    @patch.object(SystemUtilities, 'help')
    def test_use_command_help(self, mock_help):
        print(str(self.logged_in_user_data))
        mock_help.return_value = {
            "uptime": "returns the server's live time",
            "info": "returns the version number of the server and the date it was created",
            "help": "returns the list of available commands with short description",
            "logout": "to log out the User",
            "clear": " to clear the screen",
            "msg-list": "to show content of inbox",
            "msg-snd": " to create and send message",
            "msg-del [number of message]": "to delete selected message",
            "msg-show [number of message]": "to show details of message (from, date, content)"
        }

        entrance_command = {self.logged_in_user_data.logged_in_username: 'help'}
        print(entrance_command)
        result = self.command_handler.use_command(entrance_command)
        print(f'result: {result}')
        mock_help.assert_called_once()
        self.assertEqual(result, mock_help.return_value)


    #@patch('server_package.functions.SystemUtilities.stop')
    @patch.object(SystemUtilities, 'stop')
    def test_use_command_stop_without_permissions(self, mock_stop):
        print(str(self.logged_in_user_data))
        entrance_command = {self.logged_in_user_data.logged_in_username: 'stop'}
        result = self.command_handler.use_command(entrance_command)
        print(f'result: {result}')
        expected_result = {"Error": "Command unavailable. No permissions"}
        self.assertEqual(result, expected_result)
        mock_stop.assert_not_called()


class TestMenuAdminPermissions(unittest.TestCase):
    def setUp(self):
        self.logged_in_user_data = ServerUserState()
        self.logged_in_user_data.logged_in_username = 'username'
        self.logged_in_user_data.logged_in_permissions = 'admin'
        self.command_handler = CommandHandler(self.logged_in_user_data)

    #@patch('server_package.functions.SystemUtilities.help')
    @patch.object(SystemUtilities, 'help')
    def test_use_command_help(self, mock_help):
        print(str(self.logged_in_user_data))
        mock_help.return_value = {
            "uptime": "returns the server's live time",
            "info": "returns the version number of the server and the date it was created",
            "help": "returns the list of available commands with short description",
            "logout": "to log out the User",
            "clear": " to clear the screen",
            "msg-list": "to show content of inbox",
            "msg-snd": " to create and send message",
            "msg-del [number of message]": "to delete selected message",
            "msg-show [number of message]": "to show details of message (from, date, content)",
            "stop": "stops both the server and the client",
            "user-add": "create an account",
            "user-list": "shows the list of existing accounts",
            "user-del [username]": "deletes the selected account",
            "user-perm [username] [permission]": "change permissions [user] or [admin]",
            "user-stat [username] [status]": "change user status [active] or [banned]",
            "user-info [username]": "to show information about account of selected user"
        }

        entrance_command = {self.logged_in_user_data.logged_in_username: 'help'}
        result = self.command_handler.use_command(entrance_command)
        print(f'result: {result}')
        self.assertEqual(result, mock_help.return_value)
        mock_help.assert_called_once()

    #@patch('server_package.functions.SystemUtilities.stop')
    @patch.object(SystemUtilities, 'stop')
    def test_use_command_stop_with_permissions(self, mock_stop):
        print(str(self.logged_in_user_data))
        entrance_command = {self.logged_in_user_data.logged_in_username: 'stop'}
        result = self.command_handler.use_command(entrance_command)
        print(f'result: {result}')
        expected_result = {"Connection": "close"}
        self.assertEqual(result, expected_result)
        mock_stop.assert_called_once()


if __name__ == "__main__":
    unittest.main(verbosity=2)
