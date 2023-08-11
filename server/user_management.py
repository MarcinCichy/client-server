import json
from database_support import DatabaseSupport
from database_support import handle_db_file_error
import srv_response
import srv_datas


class UserManagement(DatabaseSupport):
    def __init__(self, database_support):
        self.database_support = database_support

    @staticmethod
    def user_add():
        user_add_dict_ok = {"User-add": "OK"}
        user_add_json_ok = json.dumps(user_add_dict_ok)
        return user_add_json_ok

    @handle_db_file_error
    def create_account(self, data):
        db_users = self.database_support.read_db_json(srv_datas.USERS_DATABASE)
        db_msgs = self.database_support.read_db_json(srv_datas.MESSAGES_DATABASE)

        user = {}
        new_key = None

        for dictionary in data:
            key = next(iter(dictionary))
            value = dictionary[key]
            if key == 'username':
                new_key = value
                if new_key in db_users['users']:
                    new_account_dict_nok_user= srv_response.E_ACCOUNT_EXIST
                    new_account_json_nok_user = json.dumps(new_account_dict_nok_user)
                    return new_account_json_nok_user
            elif key == "permissions":
                if value not in ['user', 'admin']:
                    new_account_dict_nok_perm = srv_response.E_WRONG_PERMISSIONS
                    new_account_json_nok_perm = json.dumps(new_account_dict_nok_perm)
                    return new_account_json_nok_perm
                else:
                    user[key] = value
            else:
                user[key] = value

        if len(new_key) > 0:
            db_users["users"][new_key] = user
            self.database_support.save_db_json(db_users, srv_datas.USERS_DATABASE)
            db_msgs['messages'][new_key] = {}
            self.database_support.save_db_json(db_msgs, srv_datas.MESSAGES_DATABASE)

            new_account_dict_ok = srv_response.NEW_ACCOUNT_CREATED
            new_account_json_ok = json.dumps(new_account_dict_ok)
            return new_account_json_ok
        else:
            new_account_dict_nok = srv_response.E_USER_NAME_NOT_PROVIDED
            new_account_json_nok = json.dumps(new_account_dict_nok)
            return new_account_json_nok

    @handle_db_file_error
    def user_list(self):
        db_users = self.database_support.read_db_json(srv_datas.USERS_DATABASE)
        users_to_list = db_users['users']
        exist_users = {}
        for key, value in users_to_list.items():
            exist_users[key] = {"permissions": value["permissions"], "status": value["status"]}
        user_show_dict = {srv_response.EXISTING_ACCOUNTS: exist_users}
        user_show_json = json.dumps(user_show_dict)
        return user_show_json

    @handle_db_file_error
    def user_info(self, username):
        db_users = self.database_support.read_db_json(srv_datas.USERS_DATABASE)
        db_msgs = self.database_support.read_db_json(srv_datas.MESSAGES_DATABASE)

        if username not in db_users['users']:
            user_to_check_dict_nok = srv_response.E_USER_DOES_NOT_EXIST
            user_to_check_json_nok = json.dumps(user_to_check_dict_nok)
            return user_to_check_json_nok
        else:
            user_to_check = db_users['users'][username]
            exist_user = {"username": username}
            for key, value in user_to_check.items():
                exist_user[key] = value
            inbox_msg_count = len(db_msgs["messages"][username])
            exist_user["inbox messages"] = inbox_msg_count
            user_info_dict = {srv_response.ACCOUNT_INFO: exist_user}
            user_info_json = json.dumps(user_info_dict)
            return user_info_json

    @handle_db_file_error
    def user_del(self, user_to_del):
        db_users = self.database_support.read_db_json(srv_datas.USERS_DATABASE)
        db_msgs = self.database_support.read_db_json(srv_datas.MESSAGES_DATABASE)
        if user_to_del not in db_users['users']:
            user_del_dict_nok = srv_response.E_USER_DOES_NOT_EXIST
            user_del_json_nok = json.dumps(user_del_dict_nok)
            return user_del_json_nok
        elif user_to_del in db_users['logged_users']:
            user_del_dict_logged = srv_response.E_USER_LOGGED_CANNOT_BE_DELETED
            user_del_json_logged = json.dumps(user_del_dict_logged)
            return user_del_json_logged
        else:
            del db_users['users'][user_to_del]
            del db_msgs['messages'][user_to_del]
            self.database_support.save_db_json(db_users, srv_datas.USERS_DATABASE)
            self.database_support.save_db_json(db_msgs, srv_datas.MESSAGES_DATABASE)
            user_del_dict = {user_to_del: srv_response.USER_DELETED}
            user_del_json = json.dumps(user_del_dict)
            return user_del_json

    @handle_db_file_error
    def user_perm(self, data):
        for user_to_change_permission, new_permissions in data.items():
            db_users = self.database_support.read_db_json(srv_datas.USERS_DATABASE)
        if user_to_change_permission not in db_users['users']:
            user_perm_dict_nok = srv_response.E_USER_DOES_NOT_EXIST
            user_perm_json_nok = json.dumps(user_perm_dict_nok)
            return user_perm_json_nok
        elif user_to_change_permission in db_users['logged_users']:
            user_perm_dict_logged = srv_response.E_USER_LOGGED_CANNOT_CHANGE_PERMISSIONS
            user_perm_json_logged = json.dumps(user_perm_dict_logged)
            return user_perm_json_logged
        elif new_permissions not in ['user', 'admin']:
            user_perm_dict_wrong = srv_response.E_WRONG_PERMISSIONS
            user_perm_json_wrong = json.dumps(user_perm_dict_wrong)
            return user_perm_json_wrong
        else:
            db_users['users'][user_to_change_permission]['permissions'] = new_permissions
            self.database_support.save_db_json(db_users, srv_datas.USERS_DATABASE)
            user_perm_dict = {user_to_change_permission: srv_response.USER_PERMISSIONS_CHANGED}
            user_perm_json = json.dumps(user_perm_dict)
            return user_perm_json

    @handle_db_file_error
    def user_stat(self, data):
        for user_to_change_status, new_status in data.items():
            db_users = self.database_support.read_db_json(srv_datas.USERS_DATABASE)
        if user_to_change_status not in db_users['users']:
            user_stat_dict_nok = srv_response.E_USER_DOES_NOT_EXIST
            user_stat_json_nok = json.dumps(user_stat_dict_nok)
            return user_stat_json_nok
        elif user_to_change_status in db_users['logged_users']:
            user_stat_dict_logged = srv_response.E_USER_LOGGED_CANNOT_CHANGE_STATUS
            user_stat_json_logged = json.dumps(user_stat_dict_logged)
            return user_stat_json_logged
        elif new_status not in ['banned', 'active']:
            user_stat_dict_wrong = srv_response.E_WRONG_STATUS
            user_stat_json_wrong = json.dumps(user_stat_dict_wrong)
            return user_stat_json_wrong
        else:
            db_users['users'][user_to_change_status]['status'] = new_status
            self.database_support.save_db_json(db_users, srv_datas.USERS_DATABASE)
            user_stat_dict = {user_to_change_status: srv_response.USER_STATUS_CHANGED}
            user_stat_json = json.dumps(user_stat_dict)
            return user_stat_json
