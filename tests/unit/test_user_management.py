import unittest
from unittest.mock import MagicMock
from server_package.user_management import UserManagement
import server_package.server_response as server_response


class TestUserManagement(unittest.TestCase):
    def setUp(self):
        self.database_support_mock = MagicMock()
        self.user_management = UserManagement(self.database_support_mock)
        self.database_support_mock.get_user.return_value = {"users":
            {
                "username1": {
                    "password": "pass",
                    "permissions": "user",
                    "status": "active",
                    "activation_date": "2023-04-06"
                },
                "logged_username": {
                    "password": "pass2",
                    "permissions": "admin",
                    "status": "active",
                    "activation_date": "2023-04-06"
                }
            },
            "logged_users": [
                "username_invalid",
                "logged_username"
    ]
        }

        self.database_support_mock.get_messages.return_value = {'messages': {
            "username1": {
                "1": {'sender': 'user2', 'date': '2023-01-01', 'content': 'Hello'},
                "2": {'sender': 'user3', 'date': '2023-01-02', 'content': 'Hi'}

            }
        }
        }

    def test_create_account_valid_data(self):
        new_username = {'username': "new_username"}
        password = {'password': "new_username_password"}
        permissions = {'permissions': "user"}
        status = {'status': "active"}
        activation_date = {'activation_date': '2023-01-01'}
        data = [new_username, password, permissions, status, activation_date]

        result = self.user_management.create_account(data)
        self.assertEqual(result, server_response.NEW_ACCOUNT_CREATED)

    def test_create_account_exist_data(self):
        new_username = {'username': "username1"}
        password = {'password': "new_username_password"}
        permissions = {'permissions': "user"}
        status = {'status': "active"}
        activation_date = {'activation_date': '2023-01-01'}
        data = [new_username, password, permissions, status, activation_date]

        result = self.user_management.create_account(data)
        self.assertEqual(result, server_response.E_ACCOUNT_EXIST)

    def test_create_account_invalid_username_data(self):
        new_username = {'username': ""}
        password = {'password': "new_username_password"}
        permissions = {'permissions': "user"}
        status = {'status': "active"}
        activation_date = {'activation_date': '2023-01-01'}
        data = [new_username, password, permissions, status, activation_date]

        result = self.user_management.create_account(data)
        self.assertEqual(result, server_response.E_USER_NAME_NOT_PROVIDED)

    def test_create_account_invalid_permissions_data(self):
        new_username = {'username': "username2"}
        password = {'password': "new_username_password"}
        permissions = {'permissions': "superuser"}
        status = {'status': "active"}
        activation_date = {'activation_date': '2023-01-01'}
        data = [new_username, password, permissions, status, activation_date]

        result = self.user_management.create_account(data)
        self.assertEqual(result, server_response.E_WRONG_PERMISSIONS)

    def test_delete_user_valid_data(self):
        user_to_del = "username1"
        result = self.user_management.user_del(user_to_del)
        self.assertEqual(result, {user_to_del: server_response.USER_DELETED})

    def test_delete_user_invalid_data(self):
        user_to_del = "username_invalid"
        result = self.user_management.user_del(user_to_del)
        self.assertEqual(result, server_response.E_USER_DOES_NOT_EXIST)

    def test_delete_logged_user(self):
        user_to_del = "username_invalid"
        result = self.user_management.user_del(user_to_del)
        self.assertEqual(result, server_response.E_USER_DOES_NOT_EXIST)

    def test_user_info_exist_user(self):
        exist_user_info = "username1"
        result = self.user_management.user_info(exist_user_info)

        mock_user_data = self.database_support_mock.get_user.return_value['users'][exist_user_info]
        mock_msg_count = len(self.database_support_mock.get_messages.return_value['messages'][exist_user_info])

        expected_result = {
            server_response.ACCOUNT_INFO: {
                'username': exist_user_info,
                'inbox messages': mock_msg_count
            }
        }

        for key, value in mock_user_data.items():
            expected_result[server_response.ACCOUNT_INFO][key] = value

        self.assertEqual(result, expected_result)

    def test_user_info_not_exist_user(self):
        not_exist_user_info = "username2"
        result = self.user_management.user_info(not_exist_user_info)
        self.assertEqual(result, server_response.E_USER_DOES_NOT_EXIST)

    def test_change_user_permissions_no_data(self):
        data = []
        result = self.user_management.user_perm(data)
        self.assertEqual(result, server_response.E_INVALID_DATA)

    def test_change_user_permissions_no_user_exist(self):
        user_to_change_permission = 'username2'
        permissions_to_change = 'admin'
        data = {user_to_change_permission: permissions_to_change}
        result = self.user_management.user_perm(data)
        self.assertEqual(result, server_response.E_USER_DOES_NOT_EXIST)

    def test_change_user_permissions_logged_user(self):
        user_to_change_permission = 'logged_username'
        permissions_to_change = 'admin'
        data = {user_to_change_permission: permissions_to_change}
        result = self.user_management.user_perm(data)
        self.assertEqual(result, server_response.E_USER_LOGGED_CANNOT_CHANGE_PERMISSIONS)

    def test_change_user_permissions_wrong_new_permissions(self):
        user_to_change_permission = 'username1'
        permissions_to_change = 'other'
        data = {user_to_change_permission: permissions_to_change}
        result = self.user_management.user_perm(data)
        self.assertEqual(result, server_response.E_WRONG_PERMISSIONS)

    def test_change_user_permissions_valid_all_data(self):
        user_to_change_permission = 'username1'
        permissions_to_change = 'admin'
        data = {user_to_change_permission: permissions_to_change}
        result = self.user_management.user_perm(data)
        self.assertEqual(result, {user_to_change_permission: server_response.USER_PERMISSIONS_CHANGED})

    # the user_stat() method is very similar to the user_perm() method, so no tests are needed.

    def test_user_list(self):
        expected_result = {server_response.EXISTING_ACCOUNTS: {
            "username1": {"permissions": "user", "status": "active"},
            "logged_username": {"permissions": "admin", "status": "active"}
        }
                           }
        result = self.user_management.user_list()
        self.assertEqual(result, expected_result)