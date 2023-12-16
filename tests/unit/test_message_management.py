import unittest
from server_package.message_management import MessageManagement
import server_package.server_response as server_response
from database_support_dummy import DatabaseSupportDummy
from server_package import server_data as server_data


class TestMessageManagement(unittest.TestCase):
    def setUp(self):
        self.db_support_dummy = DatabaseSupportDummy()
        self.msg_mgmt = MessageManagement(self.db_support_dummy)

    def test_new_message_valid_data(self):
        sender = {'sender': 'sendername'}
        date = {'date': 'YYYY-MM-DD'}
        recipient = {'recipient': 'RECIPIENT'}
        content = {'content': 'MSG CONTENT'}
        data = [sender, date, recipient, content]
        response = self.msg_mgmt.new_message(data)
        self.assertEqual(response, server_response.MESSAGE_WAS_SENT)

    def test_new_message_invalid_data(self):
        data = None
        response = self.msg_mgmt.new_message(data)
        self.assertEqual(response, server_response.E_INVALID_DATA)

    def test_new_message_full_inbox(self):
        # full_inbox = {str(i): 'message' for i in range(1, server_data.MAX_MSG_IN_INBOX + 1)}
        full_inbox = {}
        for i in range(1, server_data.MAX_MSG_IN_INBOX + 1):
            full_inbox[str(i)] = 'message'

        sender = {'sender': 'sendername'}
        date = {'date': 'YYYY-MM-DD'}
        recipient = {'recipient': 'FULL_INBOX_USER'}
        content = {'content': 'MSG CONTENT'}
        data = [sender, date, recipient, content]

        result = self.msg_mgmt.new_message(data)
        self.assertEqual(result, server_response.E_RECIPIENT_INBOX_IS_FULL)

    def test_msg_list_no_messages(self):
        result = self.msg_mgmt.msg_list('NO_MSGS_USER')
        self.assertEqual(result, {"msg": {}})

    def test_msg_list_with_messages(self):
        result = self.msg_mgmt.msg_list('RECIPIENT')
        self.assertNotEqual(result, {"msg": {}})  # ?????

    def test_msg_del_existing_message(self):
        result = self.msg_mgmt.msg_del({'RECIPIENT': '1'})
        self.assertEqual(result, server_response.MESSAGE_WAD_DELETED)

    def test_msg_del_non_existing_message(self):
        result = self.msg_mgmt.msg_del({'RECIPIENT': '7'})
        self.assertEqual(result, server_response.E_MESSAGE_NOT_FOUND)

    def test_msg_show_existing(self):
        result = self.msg_mgmt.msg_show({'RECIPIENT': '3'})
        self.assertEqual(result, {"Message to show": {'test_message_3'}})

    def test_msg_show_non_existing(self):
        result = self.msg_mgmt.msg_show({'RECIPIENT': '4'})
        self.assertEqual(result, server_response.E_MESSAGE_NOT_FOUND)

    def test_msg_count(self):
        result = self.msg_mgmt.msg_count('RECIPIENT')
        self.assertEqual(result, {"msg-inbox-count": 3})


if __name__ == '__main__':
    unittest.main(verbosity=2)
