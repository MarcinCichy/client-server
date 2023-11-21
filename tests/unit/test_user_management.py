import unittest
from unittest.mock import MagicMock
from server_package.user_management import UserManagement
import server_package.server_response as server_response


class TestMessageManagement(unittest.TestCase):
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
                }
            },
            "logged_users": [
                "nobody",
                "marcin"
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

