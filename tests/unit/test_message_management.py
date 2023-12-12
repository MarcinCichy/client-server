import unittest
from server_package.message_management import MessageManagement
import server_package.server_response as server_response


class TestMessageManagement(unittest.TestCase):
    def setUp(self):
        self.database_support_dummy = {'messages':
            {
                'RECIPIENT': {
                    "1": {'sender': 'user2', 'date': '2023-01-01', 'content': 'Hello'},
                    "2": {'sender': 'user3', 'date': '2023-01-02', 'content': 'Hi'}
                }
            }
        }
        self.msg_mgmt = MessageManagement(self.database_support_dummy)

    def test_new_message_valid_data(self):
        sender = {'sender': 'sendername'}
        date = {'date': 'YYYY-MM-DD'}
        recipient = {'recipient': 'RECIPIENT'}
        content = {'content': 'MSG CONTENT'}
        data = [sender, date, recipient, content]
        # data = ['sender', 'date', {'recipient': 'username'}, 'content']
        response = self.msg_mgmt.new_message(data)
        self.assertEqual(response, server_response.MESSAGE_WAS_SENT)

    def test_new_message_invalid_data(self):
        data = None  # Symulacja nieprawidłowych danych
        response = self.msg_mgmt.new_message(data)
        self.assertEqual(response, server_response.E_INVALID_DATA)

    # Możesz dodać więcej testów dla różnych scenariuszy


if __name__ == '__main__':
    unittest.main()

# import unittest
# from unittest.mock import MagicMock
# from server_package.message_management import MessageManagement
# from server_package import server_data as server_data
# import server_package.server_response as server_response
#
#
# class TestMessageManagement(unittest.TestCase):
#     def setUp(self):
#         self.database_support_mock = MagicMock()
#         self.message_management = MessageManagement(self.database_support_mock)
#         self.database_support_mock.get_messages.return_value = {'messages':
#             {
#                 'RECIPIENT': {
#                     "1": {'sender': 'user2', 'date': '2023-01-01', 'content': 'Hello'},
#                     "2": {'sender': 'user3', 'date': '2023-01-02', 'content': 'Hi'}
#                 }
#             }
#         }
#
#     def test_new_message_valid_data(self):
#         sender = {'sender': 'sendername'}
#         date = {'date': 'YYYY-MM-DD'}
#         recipient = {'recipient': 'RECIPIENT'}
#         content = {'content': 'MSG CONTENT'}
#         data = [sender, date, recipient, content]
#
#         result = self.message_management.new_message(data)
#         self.assertEqual(result, server_response.MESSAGE_WAS_SENT)
#
#     def test_new_message_invalid_data(self):
#         result = self.message_management.new_message(None)
#         self.assertEqual(result, server_response.E_INVALID_DATA)
#
#     def test_new_message_full_inbox(self):
#         # full_inbox = {str(i): 'message' for i in range(1, server_data.MAX_MSG_IN_INBOX + 1)}
#         full_inbox = {}
#         for i in range(1, server_data.MAX_MSG_IN_INBOX + 1):
#             full_inbox[str(i)] = 'message'
#         self.database_support_mock.get_messages.return_value = {'messages': {'FULL_INBOX_USER': full_inbox}}
#
#         sender = {'sender': 'sendername'}
#         date = {'date': 'YYYY-MM-DD'}
#         recipient = {'recipient': 'FULL_INBOX_USER'}
#         content = {'content': 'MSG CONTENT'}
#         data = [sender, date, recipient, content]
#
#         result = self.message_management.new_message(data)
#         self.assertEqual(result, server_response.E_RECIPIENT_INBOX_IS_FULL)
#
#     def test_msg_list_no_messages(self):
#         self.database_support_mock.get_messages.return_value = {'messages': {'username': {}}}
#         result = self.message_management.msg_list('username')
#         self.assertEqual(result, {"msg": {}})
#
#     def test_msg_list_with_messages(self):
#         result = self.message_management.msg_list('RECIPIENT')
#         self.assertNotEqual(result, {"msg": {}})
#
#     def test_msg_del_existing_message(self):
#         self.database_support_mock.get_messages.return_value = {'messages': {'username': {'1': 'message1'}}}
#         result = self.message_management.msg_del({'username': '1'})
#         self.assertEqual(result, server_response.MESSAGE_WAD_DELETED)
#
#     def test_msg_del_non_existing_message(self):
#         self.database_support_mock.get_messages.return_value = {'messages': {'username': {}}}
#         result = self.message_management.msg_del({'username': '1'})
#         self.assertEqual(result, server_response.E_MESSAGE_NOT_FOUND)
#
#     def test_msg_show_existing(self):
#         self.database_support_mock.get_messages.return_value = {'messages': {'username': {'1': 'message1'}}}
#         result = self.message_management.msg_show({'username': '1'})
#         self.assertEqual(result, {"Message to show": 'message1'})
#
#     def test_msg_show_non_existing(self):
#         self.database_support_mock.get_messages.return_value = {'messages': {'username': {}}}
#         result = self.message_management.msg_show({'username': '1'})
#         self.assertEqual(result, server_response.E_MESSAGE_NOT_FOUND)
#
#     def test_msg_count(self):
#         self.database_support_mock.get_messages.return_value = {
#             'messages': {'username': {'1': 'message1', '2': 'message2'}}}
#         result = self.message_management.msg_count('username')
#         self.assertEqual(result, {"msg-inbox-count": 2})
#
#
# if __name__ == "__main__":
#     unittest.main(verbosity=2)