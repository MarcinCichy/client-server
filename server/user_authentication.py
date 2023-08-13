import json

import server_data
import server_response
from database_support import DatabaseSupport
from database_support import handle_db_file_error


class UserAuthentication(DatabaseSupport):
    def __init__(self, database_support):
        self.database_support = database_support

    @handle_db_file_error
    def get_user_data(self, login_username):
        db_users = self.database_support.read_db_json(server_data.USERS_DATABASE)
        if login_username in db_users["users"]:
            return db_users["users"][login_username]
        else:
            return None

    @handle_db_file_error
    def login(self, login_data):
        login_username = login_data[0]['username']
        login_password = login_data[1]['password']

        user_data = self.get_user_data(login_username)
        if user_data is not None and user_data['status'] == "active" and user_data['password'] == login_password:
            print(f'Access granted to {login_username}')
            db_users = self.database_support.read_db_json(server_data.USERS_DATABASE)
            if login_username in db_users['logged_users']:
                db_users['logged_users'].remove(login_username)
            db_users['logged_users'].append(login_username)
            self.database_support.save_db_json(db_users, server_data.USERS_DATABASE)
            login_dict_ok = {"Login": "OK", "login_username": login_username, "user_permissions": user_data['permissions']}
            login_json_ok = json.dumps(login_dict_ok)
            return login_json_ok
        elif user_data is not None and user_data['status'] == "banned":
            print(f'Access denied to {login_username}, user banned')
            login_dict_baned = server_response.E_USER_IS_BANNED
            login_json_baned = json.dumps(login_dict_baned)
            return login_json_baned
        else:
            print(f'Access denied to {login_username}')
            login_dict_nok = server_response.E_INVALID_CREDENTIALS
            login_json_nok = json.dumps(login_dict_nok)
            return login_json_nok

    @handle_db_file_error
    def logout(self, logout_data):
        db_users = self.database_support.read_db_json(server_data.USERS_DATABASE)

        if logout_data in db_users['logged_users']:
            db_users['logged_users'].remove(logout_data)
            self.database_support.save_db_json(db_users, server_data.USERS_DATABASE)
            print(f'{logout_data} is logged out')
            logout_dict = {"Logout": "Successful"}
            logout_json = json.dumps(logout_dict)
            return logout_json
        else:
            pass

    @handle_db_file_error
    def get_permissions(self, username):
        user_data = self.get_user_data(username)
        if user_data is not None:
            return user_data['permissions']
        else:
            return None

