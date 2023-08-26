import server_data
import server_response
from database_support import DatabaseSupport


class UserAuthentication(DatabaseSupport):
    def __init__(self, database_support):
        self.database_support = database_support

    def get_user_data(self, login_username):
        db_users = self.database_support.read_db_json(server_data.USERS_DATABASE)
        if login_username in db_users["users"]:
            return db_users["users"][login_username]
        else:
            return None

    def login(self, login_data):
        login_username = login_data[0]['username']
        login_password = login_data[1]['password']

        user_data = self.get_user_data(login_username)
        if user_data is not None and user_data['status'] == "active" and user_data['password'] == login_password:
            print(f'Access granted to {login_username}')
            #  these three lines below are needed to prevent multiplication of the username added to the key logged_user
            #  in case the connection with the server is lost and re-established or the client-side application
            #  stops working and will be restarted
            user_logged = self.database_support.read_db_json(server_data.USERS_DATABASE)
            if login_username in user_logged['logged_users']:
                user_logged['logged_users'].remove(login_username)
            user_logged['logged_users'].append(login_username)
            self.database_support.save_db_json(user_logged, server_data.USERS_DATABASE)
            return {"Login": "OK", "login_username": login_username, "user_permissions": user_data['permissions']}
        elif user_data is not None and user_data['status'] == "banned":
            print(f'Access denied to {login_username}, user banned')
            return server_response.E_USER_IS_BANNED
        else:
            print(f'Access denied to {login_username}')
            return server_response.E_INVALID_CREDENTIALS

    def logout(self, logout_data):
        db_users = self.database_support.read_db_json(server_data.USERS_DATABASE)

        if logout_data in db_users['logged_users']:
            db_users['logged_users'].remove(logout_data)
            self.database_support.save_db_json(db_users, server_data.USERS_DATABASE)
            print(f'{logout_data} is logged out')
            return {"Logout": "Successful"}
        else:
            pass

    def get_permissions(self, username):
        user_data = self.get_user_data(username)
        if user_data is not None:
            return user_data['permissions']
        else:
            return None

