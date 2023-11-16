import unittest
from unittest.mock import MagicMock
from server_package.message_management import MessageManagement
import server_package.server_response as server_response



class TestMessageManagement(unittest.TestCase):
    def setUp(self):
        self.database_support_mock = MagicMock()
        self.message_management = MessageManagement(self.database_support_mock)

    def test_new_message_valid_data(self):
        self.database_support_mock.get_messages.return_value = {'messages': {}}
        result = self.message_management.new_message(['sender', 'date', {'recipient': 'username'}, 'content'])
        self.assertEqual(result, server_response.MESSAGE_WAS_SENT)

    def test_new_message_invalid_data(self):
        result = self.message_management.new_message(None)
        self.assertEqual(result, server_response.E_INVALID_DATA)

    def test_msg_list_no_messages(self):
        self.database_support_mock.get_messages.return_value = {'messages': {'username': {}}}
        result = self.message_management.msg_list('username')
        self.assertEqual(result, {"msg": {}})

    def test_msg_list_with_messages(self):
        self.database_support_mock.get_messages.return_value = {'messages': {'username': {'1': 'message1'}}}
        result = self.message_management.msg_list('username')
        self.assertNotEqual(result, {"msg": {}})

