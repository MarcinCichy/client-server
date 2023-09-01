import server_data
import server_response
from database_support import DatabaseSupport
from database_support import handle_db_file_error


class UserAuthentication:
    def __init__(self, logged_in_user_data):
        self.logged_in_user_data = logged_in_user_data
        self.database_support = DatabaseSupport()
        self.logged_in_username = None
        self.logged_in_permissions = None

    @handle_db_file_error
    def get_user_data(self, login_username):
        db_users = self.database_support.read_db_json(server_data.USERS_DATABASE)
        print(f'DB_USERS from get_user_data = {db_users}')
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
            #  these three lines below are needed to prevent multiplication of the username added to the key logged_user
            #  in case the connection with the server is lost and re-established or the client-side application
            #  stops working and will be restarted
            # ----------------------------------------------------------------------------------
            user_logged = self.database_support.read_db_json(server_data.USERS_DATABASE)
            if login_username in user_logged['logged_users']:
                user_logged['logged_users'].remove(login_username)
            # ----------------------------------------------------------------------------------
            user_logged['logged_users'].append(login_username)
            self.database_support.save_db_json(user_logged, server_data.USERS_DATABASE)
            self.logged_in_username = user_logged['logged_users']
            self.logged_in_permissions = user_data['permissions']
            self.logged_in_user_data.set_user_data(self.logged_in_username, self.logged_in_permissions)
            return {"Login": "OK", "login_username": login_username, "user_permissions": user_data['permissions']}
        elif user_data is not None and user_data['status'] == "banned":
            print(f'Access denied to {login_username}, user banned')
            return server_response.E_USER_IS_BANNED
        else:
            print(f'Access denied to {login_username}, invalid credentials')
            return server_response.E_INVALID_CREDENTIALS

    @handle_db_file_error
    def logout(self, logout_data):
        db_users = self.database_support.read_db_json(server_data.USERS_DATABASE)

        if logout_data in db_users['logged_users']:
            db_users['logged_users'].remove(logout_data)
            self.database_support.save_db_json(db_users, server_data.USERS_DATABASE)
            print(f'{logout_data} is logged out')
            self.logged_in_user_data.clear_user_data()
            return {"Logout": "Successful"}
        else:
            pass

