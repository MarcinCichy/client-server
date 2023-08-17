import json

import server_data
import server_response
from database_support import DatabaseSupport
from database_support import handle_db_file_error


class UserManagement(DatabaseSupport):
    def __init__(self, database_support):
        self.database_support = database_support

    @staticmethod
    def user_add():
        return json.dumps({"User-add": "OK"})

    @handle_db_file_error
    def create_account(self, data):
        db_users = self.database_support.read_db_json(server_data.USERS_DATABASE)
        db_msgs = self.database_support.read_db_json(server_data.MESSAGES_DATABASE)

        user = {}
        new_key = None

        for dictionary in data:
            key = next(iter(dictionary))
            value = dictionary[key]
            if key == 'username':
                new_key = value
                if new_key in db_users['users']:
                    return json.dumps(server_response.E_ACCOUNT_EXIST)
            elif key == "permissions":
                if value not in ['user', 'admin']:
                    return json.dumps(server_response.E_WRONG_PERMISSIONS)
                else:
                    user[key] = value
            else:
                user[key] = value

        if len(new_key) > 0:
            db_users["users"][new_key] = user
            self.database_support.save_db_json(db_users, server_data.USERS_DATABASE)
            db_msgs['messages'][new_key] = {}
            self.database_support.save_db_json(db_msgs, server_data.MESSAGES_DATABASE)
            return json.dumps(server_response.NEW_ACCOUNT_CREATED)
        else:
            return json.dumps(server_response.E_USER_NAME_NOT_PROVIDED)

    @handle_db_file_error
    def user_list(self):
        db_users = self.database_support.read_db_json(server_data.USERS_DATABASE)
        users_to_list = db_users['users']
        exist_users = {}
        for key, value in users_to_list.items():
            exist_users[key] = {"permissions": value["permissions"], "status": value["status"]}
        return json.dumps({server_response.EXISTING_ACCOUNTS: exist_users})

    @handle_db_file_error
    def user_info(self, username):
        db_users = self.database_support.read_db_json(server_data.USERS_DATABASE)
        db_msgs = self.database_support.read_db_json(server_data.MESSAGES_DATABASE)

        if username not in db_users['users']:
            return json.dumps(server_response.E_USER_DOES_NOT_EXIST)
        else:
            user_to_check = db_users['users'][username]
            exist_user = {"username": username}
            for key, value in user_to_check.items():
                exist_user[key] = value
            inbox_msg_count = len(db_msgs["messages"][username])
            exist_user["inbox messages"] = inbox_msg_count
            return json.dumps({server_response.ACCOUNT_INFO: exist_user})

    @handle_db_file_error
    def user_del(self, user_to_del):
        db_users = self.database_support.read_db_json(server_data.USERS_DATABASE)
        db_msgs = self.database_support.read_db_json(server_data.MESSAGES_DATABASE)
        if user_to_del not in db_users['users']:
            return json.dumps(server_response.E_USER_DOES_NOT_EXIST)
        elif user_to_del in db_users['logged_users']:
            return json.dumps(server_response.E_USER_LOGGED_CANNOT_BE_DELETED)
        else:
            del db_users['users'][user_to_del]
            del db_msgs['messages'][user_to_del]
            self.database_support.save_db_json(db_users, server_data.USERS_DATABASE)
            self.database_support.save_db_json(db_msgs, server_data.MESSAGES_DATABASE)
            return json.dumps({user_to_del: server_response.USER_DELETED})

    @handle_db_file_error
    def user_perm(self, data):
        for user_to_change_permission, new_permissions in data.items():
            db_users = self.database_support.read_db_json(server_data.USERS_DATABASE)
        if user_to_change_permission not in db_users['users']:
            return json.dumps(server_response.E_USER_DOES_NOT_EXIST)
        elif user_to_change_permission in db_users['logged_users']:
            return json.dumps(server_response.E_USER_LOGGED_CANNOT_CHANGE_PERMISSIONS)
        elif new_permissions not in ['user', 'admin']:
            return json.dumps(server_response.E_WRONG_PERMISSIONS)
        else:
            db_users['users'][user_to_change_permission]['permissions'] = new_permissions
            self.database_support.save_db_json(db_users, server_data.USERS_DATABASE)
            return json.dumps({user_to_change_permission: server_response.USER_PERMISSIONS_CHANGED})

    @handle_db_file_error
    def user_stat(self, data):
        for user_to_change_status, new_status in data.items():
            db_users = self.database_support.read_db_json(server_data.USERS_DATABASE)
        if user_to_change_status not in db_users['users']:
            return json.dumps(server_response.E_USER_DOES_NOT_EXIST)
        elif user_to_change_status in db_users['logged_users']:
            return json.dumps(server_response.E_USER_LOGGED_CANNOT_CHANGE_STATUS)
        elif new_status not in ['banned', 'active']:
            return json.dumps(server_response.E_WRONG_STATUS)
        else:
            db_users['users'][user_to_change_status]['status'] = new_status
            self.database_support.save_db_json(db_users, server_data.USERS_DATABASE)
            return json.dumps({user_to_change_status: server_response.USER_STATUS_CHANGED})
