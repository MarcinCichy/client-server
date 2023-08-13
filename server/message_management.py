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
        msg_snd_dict_ok = {'Msg-snd': "OK"}
        msg_snd_json_ok = json.dumps(msg_snd_dict_ok)
        return msg_snd_json_ok

    @handle_db_file_error
    def new_message(self, data):
        db_msgs = self.database_support.read_db_json(server_data.MESSAGES_DATABASE)

        sender = data[0]
        date = data[1]
        recipient = data[2]
        content = data[3]
        username = recipient["recipient"]

        if recipient["recipient"] not in db_msgs["messages"].keys():
            msg_snd_error = server_response.E_RECIPIENT_DOES_NOT_EXIST
            msg_snd_error_json = json.dumps(msg_snd_error)
            return msg_snd_error_json
        elif len(db_msgs["messages"][username]) == 5:
            msg_snd_error = server_response.E_RECIPIENT_INBOX_IS_FULL
            msg_snd_error_json = json.dumps(msg_snd_error)
            return msg_snd_error_json
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
            msgs_snd_dict = server_response.MESSAGE_WAS_SENT
            msgs_snd_json = json.dumps(msgs_snd_dict)
            return msgs_snd_json

    @handle_db_file_error
    def msg_list(self, username):  # to show all messages in box in middle window show all msgs in box
        db_msgs = self.database_support.read_db_json(server_data.MESSAGES_DATABASE)
        all_inbox_msgs = db_msgs['messages'][username]

        new_dict = {}
        for message_number, message_data in all_inbox_msgs.items():
            if isinstance(message_data, dict) and 'sender' in message_data and 'date' in message_data:
                new_dict[message_number] = {'sender': message_data['sender'], 'date': message_data['date']}
        all_msg_dict = {"msg": new_dict}
        all_msg_json = json.dumps(all_msg_dict)
        return all_msg_json

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
                msgs_del_dict = server_response.MESSAGE_WAD_DELETED
                msgs_del_json = json.dumps(msgs_del_dict)
                return msgs_del_json
            else:
                return json.dumps(server_response.E_MESSAGE_NOT_FOUND)

    @handle_db_file_error
    def msg_show(self, data):  # to show selected message
        db_msgs = self.database_support.read_db_json(server_data.MESSAGES_DATABASE)
        for username, msg_num in data.items():
            if msg_num in db_msgs['messages'][username]:
                message_to_show = db_msgs['messages'][username][msg_num]
                msgs_to_show_dict = {"Message to show": message_to_show}
                msgs_to_show_json = json.dumps(msgs_to_show_dict)
                return msgs_to_show_json
            else:
                return json.dumps(server_response.E_MESSAGE_NOT_FOUND)

    @handle_db_file_error
    def msg_count(self, username):  # to count all messages in box
        db_msgs = self.database_support.read_db_json(server_data.MESSAGES_DATABASE)
        inbox_msg_count = len(db_msgs["messages"][username])
        if inbox_msg_count >= 5:
            inbox_msg_count = str(inbox_msg_count) + server_response.YOUR_INBOX_IS_FULL
        inbox_msg_count_dict = {"msg-inbox-count": inbox_msg_count}
        inbox_msg_count_json = json.dumps(inbox_msg_count_dict)
        return inbox_msg_count_json

