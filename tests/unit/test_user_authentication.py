import unittest
from unittest.mock import MagicMock
from server_package.user_authentication import UserAuthentication
import server_package.server_response as server_response


class TestUserAuthentication(unittest.TestCase):
    def setUp(self):
        self.database_support_mock = MagicMock()
        self.logged_in_user_data_mock = self.database_support_mock.get_user.return_value
        self.user_auth = UserAuthentication(self.logged_in_user_data_mock, self.database_support_mock)
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
                    "status": "banned",
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

    def test_login_user_no_login_data(self):
        data = []
        result = self.user_auth.login(data)
        self.assertEqual(result, server_response.E_INVALID_DATA)

    def test_login_user_valid_data(self):
        valid_login_data = [{"username": "username1"}, {"password": "pass"}]
        expected = {"Login": "OK", "login_username": "username1", "user_permissions": "user"}
        result = self.user_auth.login(valid_login_data)
        self.assertEqual(result, expected)

    def test_login_banned_user(self):
        banned_user_data = [{"username": "logged_username"}, {"password": "pass2"}]
        expected = server_response.E_USER_IS_BANNED
        result = self.user_auth.login(banned_user_data)
        self.assertEqual(result, expected)

    def test_login_user_no_valid_data(self):
        no_valid_login_data = [{"username": "username1"}, {"password": "pass3"}]
        expected = server_response.E_INVALID_CREDENTIALS
        result = self.user_auth.login(no_valid_login_data)
        self.assertEqual(result, expected)

    def test_logout_user_no_data(self):
        data = []
        expected = server_response.E_INVALID_DATA
        result = self.user_auth.logout(data)
        self.assertEqual(result, expected)

    def test_logout_user_logged_in_user(self):
        data = "username_invalid"
        expected = {"Logout": "Successful"}
        result = self.user_auth.logout(data)
        self.assertEqual(result, expected),

    def test_logout_user_no_logged_user(self):
        data = "username_not_exist"
        expected = None
        result = self.user_auth.logout(data)
        self.assertEqual(result, expected)