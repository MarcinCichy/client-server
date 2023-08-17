import json
from database_support import DatabaseSupport
from database_support import handle_db_file_error
import server_response
import server_data


class MessageManagement(DatabaseSupport):
    def __init__(self, database_support):
        self.database_support = database_support

    @staticmethod
    def msg_snd():
        return json.dumps({'Msg-snd': "OK"})

    @handle_db_file_error
    def new_message(self, data):
        db_msgs = self.database_support.read_db_json(server_data.MESSAGES_DATABASE)

        sender = data[0]
        date = data[1]
        recipient = data[2]
        content = data[3]
        username = recipient["recipient"]

        if recipient["recipient"] not in db_msgs["messages"].keys():
            return json.dumps(server_response.E_RECIPIENT_DOES_NOT_EXIST)
        elif len(db_msgs["messages"][username]) == 5:
            return json.dumps(server_response.E_RECIPIENT_INBOX_IS_FULL)
        else:
            inbox_msg_count = len(db_msgs["messages"][username])
            inbox_msg_count += 1
            new_tem_dict = {
                **sender,
                **date,
                **content
            }
            db_msgs["messages"][username][inbox_msg_count] = new_tem_dict
            self.database_support.save_db_json(db_msgs, server_data.MESSAGES_DATABASE)
            return json.dumps(server_response.MESSAGE_WAS_SENT)

    @handle_db_file_error
    def msg_list(self, username):  # to show all messages in box in middle window show all msgs in box
        db_msgs = self.database_support.read_db_json(server_data.MESSAGES_DATABASE)
        all_inbox_msgs = db_msgs['messages'][username]

        msg_list_dict = {}
        for message_number, message_data in all_inbox_msgs.items():
            if isinstance(message_data, dict) and 'sender' in message_data and 'date' in message_data:
                msg_list_dict[message_number] = {'sender': message_data['sender'], 'date': message_data['date']}
        return json.dumps({"msg": msg_list_dict})

    @handle_db_file_error
    def msg_del(self, data):  # to delete selected message
        db_msgs = self.database_support.read_db_json(server_data.MESSAGES_DATABASE)
        for username, msg_num in data.items():
            if msg_num in db_msgs['messages'][username]:
                del db_msgs['messages'][username][msg_num]
                updated_msgs = {}
                new_num = 1
                for num, msg in db_msgs['messages'][username].items():
                    if int(num) != int(msg_num):
                        updated_msgs[str(new_num)] = msg
                        new_num += 1
                db_msgs['messages'][username] = updated_msgs
                self.database_support.save_db_json(db_msgs, server_data.MESSAGES_DATABASE)
                return json.dumps(server_response.MESSAGE_WAD_DELETED)
            else:
                return json.dumps(server_response.E_MESSAGE_NOT_FOUND)

    @handle_db_file_error
    def msg_show(self, data):  # to show selected message
        db_msgs = self.database_support.read_db_json(server_data.MESSAGES_DATABASE)
        for username, msg_num in data.items():
            if msg_num in db_msgs['messages'][username]:
                message_to_show = db_msgs['messages'][username][msg_num]
                return json.dumps({"Message to show": message_to_show})
            else:
                return json.dumps(server_response.E_MESSAGE_NOT_FOUND)

    @handle_db_file_error
    def msg_count(self, username):  # to count all messages in box
        db_msgs = self.database_support.read_db_json(server_data.MESSAGES_DATABASE)
        inbox_msg_count = len(db_msgs["messages"][username])
        if inbox_msg_count >= 5:
            inbox_msg_count = str(inbox_msg_count) + server_response.YOUR_INBOX_IS_FULL
        return json.dumps({"msg-inbox-count": inbox_msg_count})

