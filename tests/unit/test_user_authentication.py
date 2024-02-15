import unittest
from server_package.user_authentication import UserAuthentication
import server_package.server_response as server_response
from server_package.database_support import DatabaseSupport


class TestUserAuthentication(unittest.TestCase):
    def setUp(self):
        self.database_support = DatabaseSupport()
        self.user_auth = UserAuthentication(self.database_support)

    def test_login_user_no_login_data(self):
        no_data = []
        result = self.user_auth.login(no_data)
        self.assertEqual(result, server_response.E_INVALID_DATA)

    def test_login_user_valid_data(self):
        valid_login_data = [{"username": "RECIPIENT"}, {"password": "pass"}]
        expected = {"Login": "OK", "login_username": "RECIPIENT", "user_permissions": "user"}
        result = self.user_auth.login(valid_login_data)
        self.assertEqual(result, expected)

    def test_login_banned_user(self):
        banned_user_data = [{"username": "other_user"}, {"password": "pass2"}]
        expected = server_response.E_USER_IS_BANNED
        result = self.user_auth.login(banned_user_data)
        self.assertEqual(result, expected)

    def test_login_user_no_valid_data(self):
        no_valid_login_data = [{"username": "RECIPIENT"}, {"password": "pass3"}]
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


if __name__ == '__main__':
    unittest.main(verbosity=2)
