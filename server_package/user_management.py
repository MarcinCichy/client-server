import server_package.server_response as server_response
from server_package.database_support import handle_db_file_error


class UserManagement:
    def __init__(self, database_support):
        self.database_support = database_support

    @staticmethod
    def user_add():
        return {"User-add": "OK"}

    @handle_db_file_error
    def create_account(self, data):
        db_users = self.database_support.get_user()
        db_msgs = self.database_support.get_messages()

        new_user = {}
        new_key = None

        for dictionary in data:
            key = next(iter(dictionary))
            value = dictionary[key]
            if key == 'username':
                new_key = value
                if new_key in db_users['users']:
                    return server_response.E_ACCOUNT_EXIST
            elif key == "permissions":
                if value not in ['user', 'admin']:
                    return server_response.E_WRONG_PERMISSIONS
                else:
                    new_user[key] = value
            else:  # this is for all others keys in dictionary, as: 'password', 'status, 'activation_date'
                new_user[key] = value

        if len(new_key) > 0:
            db_users["users"][new_key] = new_user
            self.database_support.save_user(db_users)
            db_msgs['messages'][new_key] = {}
            self.database_support.save_messages(db_msgs)
            return server_response.NEW_ACCOUNT_CREATED
        else:
            return server_response.E_USER_NAME_NOT_PROVIDED

    @handle_db_file_error
    def user_del(self, user_to_del):
        db_users = self.database_support.get_user()
        db_msgs = self.database_support.get_messages()
        if user_to_del not in db_users['users']:
            return server_response.E_USER_DOES_NOT_EXIST
        elif user_to_del in db_users['logged_users']:
            return server_response.E_USER_LOGGED_CANNOT_BE_DELETED
        else:
            del db_users['users'][user_to_del]
            del db_msgs['messages'][user_to_del]
            self.database_support.save_user(db_users)
            self.database_support.save_messages(db_msgs)
            return {user_to_del: server_response.USER_DELETED}

    @handle_db_file_error
    def user_list(self):
        db_users = self.database_support.get_user()  #***************************
        users_to_list = db_users['users']
        exist_users = {}
        for key, value in users_to_list.items():
            exist_users[key] = {"permissions": value["permissions"], "status": value["status"]}
        return {server_response.EXISTING_ACCOUNTS: exist_users}

    # def user_info(self, username):
    #     db_users = self.database_support.get_user()
    #     db_msgs = self.database_support.get_messages()
    #
    #     if username not in db_users['users']:
    #         return server_response.E_USER_DOES_NOT_EXIST
    #     else:
    #         user_to_check = db_users['users'][username]
    #         exist_user = {"username": username}
    #         for key, value in user_to_check.items():
    #             exist_user[key] = value
    #         inbox_msg_count = len(db_msgs["messages"][username])
    #         exist_user["inbox messages"] = inbox_msg_count
    #         return {server_response.ACCOUNT_INFO: exist_user}

    def user_info(self, username):
        db_users = self.database_support.get_user()
        db_msgs = self.database_support.get_messages()

        if username not in db_users['users']:
            return server_response.E_USER_DOES_NOT_EXIST
        else:
            user_to_check = db_users['users'][username]
            exist_user = {"username": username}
            for key, value in user_to_check.items():
                exist_user[key] = value
            inbox_msg_count = len(db_msgs["messages"][username])
            exist_user["inbox messages"] = inbox_msg_count
            return {server_response.ACCOUNT_INFO: exist_user}


    @handle_db_file_error
    def user_perm(self, data):
        if not data:
            return server_response.E_INVALID_DATA
        else:
            user_to_change_permission, new_permissions = next(iter(data.items()))
            print(f'User name to change permissions: {user_to_change_permission}, to new permissions: {new_permissions}')

        if self.database_support.check_if_user_exist(user_to_change_permission):
            return server_response.E_USER_DOES_NOT_EXIST
        # elif user_to_change_status in db_users['logged_users']:
        #     return server_response.E_USER_LOGGED_CANNOT_CHANGE_STATUS
        elif new_permissions not in ['user', 'admin']:
            return server_response.E_WRONG_PERMISSIONS
        else:
            self.database_support.data_update('users', 'permissions', user_to_change_permission, new_permissions)
            return {user_to_change_permission: server_response.USER_PERMISSIONS_CHANGED}


    @handle_db_file_error
    def user_stat(self, data):
        if not data:
            return server_response.E_INVALID_DATA
        else:
            user_to_change_status, new_status = next(iter(data.items()))
            print(f'User name to change status: {user_to_change_status}, to new status: {new_status}')

        if self.database_support.check_if_user_exist(user_to_change_status):
            return server_response.E_USER_DOES_NOT_EXIST
        # elif user_to_change_status in db_users['logged_users']:
        #     return server_response.E_USER_LOGGED_CANNOT_CHANGE_STATUS
        elif new_status not in ['banned', 'active']:
            return server_response.E_WRONG_STATUS
        else:
            self.database_support.data_update('users', 'status', user_to_change_status, new_status)
            return {user_to_change_status: server_response.USER_STATUS_CHANGED}

