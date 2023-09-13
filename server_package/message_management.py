from database_support import handle_db_file_error
import server_response
import server_data


class MessageManagement:
    def __init__(self, database_support):
        self.database_support = database_support

    @staticmethod
    def msg_snd():
        return {'Msg-snd': "OK"}

    @handle_db_file_error
    def new_message(self, data):
        if not data:
            return server_response.E_INVALID_DATA

        db_msgs = self.database_support.get_messages()

        sender = data[0]
        date = data[1]
        recipient = data[2]
        content = data[3]
        username = recipient["recipient"]

        if username not in db_msgs["messages"].keys():
            return server_response.E_RECIPIENT_DOES_NOT_EXIST
        elif len(db_msgs["messages"][username]) == server_data.MAX_MSG_IN_INBOX:
            return server_response.E_RECIPIENT_INBOX_IS_FULL
        else:
            inbox_msg_count = len(db_msgs["messages"][username])
            inbox_msg_count += 1
            new_temp_dict = {
                **sender,
                **date,
                **content
            }
            db_msgs["messages"][username][inbox_msg_count] = new_temp_dict
            self.database_support.save_messages(db_msgs)
            return server_response.MESSAGE_WAS_SENT

    @handle_db_file_error
    def msg_list(self, username):  # to show all messages in box in middle window show all msgs in box
        if not username:
            return server_response.E_INVALID_DATA

        db_msgs = self.database_support.get_messages()
        all_inbox_msgs = db_msgs['messages'][username]

        msg_list_dict = {}
        for message_number, message_data in all_inbox_msgs.items():
            if isinstance(message_data, dict) and 'sender' in message_data and 'date' in message_data:
                msg_list_dict[message_number] = {'sender': message_data['sender'], 'date': message_data['date']}
        return {"msg": msg_list_dict}

    @handle_db_file_error
    def msg_del(self, data):  # to delete selected message
        if not data:
            return server_response.E_INVALID_DATA

        db_msgs = self.database_support.get_messages()
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
                self.database_support.save_messages(db_msgs)
                return server_response.MESSAGE_WAD_DELETED
            else:
                return server_response.E_MESSAGE_NOT_FOUND

    @handle_db_file_error
    def msg_show(self, data):  # to show selected message
        if not data:
            return server_response.E_INVALID_DATA

        db_msgs = self.database_support.get_messages()
        for username, msg_num in data.items():
            if msg_num in db_msgs['messages'][username]:
                message_to_show = db_msgs['messages'][username][msg_num]
                return {"Message to show": message_to_show}
            else:
                return server_response.E_MESSAGE_NOT_FOUND

    @handle_db_file_error
    def msg_count(self, username):  # to count all messages in inbox
        if not username:
            return server_response.E_INVALID_DATA

        db_msgs = self.database_support.get_messages()
        inbox_msg_count = len(db_msgs["messages"][username])
        if inbox_msg_count >= 5:
            inbox_msg_count = str(inbox_msg_count) + server_response.YOUR_INBOX_IS_FULL
        return {"msg-inbox-count": inbox_msg_count}

