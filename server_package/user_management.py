import datetime
import server_package.server_response as server_response
from server_package.database_support import handle_db_file_error



class UserManagement:
    def __init__(self, database_support):
        self.database_support = database_support

    @staticmethod
    def user_add():
        return {"User-add": "OK"}

    @handle_db_file_error

    #  INSERT INTO users (user_name, password, permissions, status, activation_date, login_time)
    # SELECT user_name, password, permissions, status, activation_date, login_time
    # FROM users;

    # Dane z add user: [{'username': 'atos'}, {'password': 'portos'}, {'permissions': 'user'},
    # {'status': 'active'}, {'activation_date': '2024-01-31'}]

    def create_account(self, data):
        # db_users = self.database_support.get_user()
        # db_msgs = self.database_support.get_messages()

        new_user = {}
        new_key = None

        print(f'Dane z add user: {data}')

        lista_wartosci = [list(d.values())[0] for d in data]

        print(lista_wartosci)
        print(type(lista_wartosci))

        username = lista_wartosci[0]

        if not data:
            return server_response.E_INVALID_DATA

        if self.database_support.check_if_user_exist(username):
            return server_response.E_ACCOUNT_EXIST
        else:
            self.database_support.create_db_account('users', lista_wartosci)


        # for dictionary in data:
        #     lista_wartosci = list(data.values())
        #     print(lista_wartosci)
        #     print(type(lista_wartosci))


        #     key = next(iter(dictionary))
        #     value = dictionary[key]
        #     if key == 'username':
        #         new_key = value
        #         if self.database_support.check_if_user_exist(new_key):
        #             return server_response.E_ACCOUNT_EXIST
        #     elif key == "permissions":
        #         if value not in ['user', 'admin']:
        #             return server_response.E_WRONG_PERMISSIONS
        #         else:
        #             new_user[key] = value
        #     else:  # this is for all others keys in dictionary, as: 'password', 'status, 'activation_date'
        #         new_user[key] = value
        #
        # print(new_user)
        # print(type(new_user))
        # lista_wartosci = list(new_user.values())
        # print(lista_wartosci)
        # print(type(lista_wartosci))
    """
        if len(new_key) > 0:
            # db_users["users"][new_key] = new_user
            # self.database_support.save_user(db_users)
            # db_msgs['messages'][new_key] = {}
            # self.database_support.save_messages(db_msgs)
            self.database_support.create_account(new_user)
            return server_response.NEW_ACCOUNT_CREATED
        else:
            return server_response.E_USER_NAME_NOT_PROVIDED
    """
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
        all_user_data = self.database_support.get_all_users_list()
        users_dict = {}
        for row in all_user_data:
            user_name, permissions, status = row
            users_dict[user_name] = {'permissions': permissions, 'status': status}
        return {server_response.EXISTING_ACCOUNTS: users_dict}

    def user_info(self, username):
        if not self.database_support.check_if_user_exist(username):
            return server_response.E_USER_DOES_NOT_EXIST
        else:
            selected_user_data = self.database_support.get_info_about_user(username)
            new_selected_user_data = {'user': selected_user_data.pop('user_name')}
            new_selected_user_data.update(selected_user_data)
            new_selected_user_data['activation_date'] = self.convert_datetime_date_to_string_date(selected_user_data['activation_date'])
            inbox_msg_count = self.database_support.inbox_msg_counting(username)
            new_selected_user_data["inbox messages"] = inbox_msg_count
            new_selected_user_data['login_time'] = self.convert_datetime_datetime_to_string_date(selected_user_data['login_time'])

            return {server_response.ACCOUNT_INFO: new_selected_user_data}


    @handle_db_file_error
    def user_perm(self, data):
        if not data:
            return server_response.E_INVALID_DATA
        else:
            user_to_change_permission, new_permissions = next(iter(data.items()))
            print(f'User name to change permissions: {user_to_change_permission}, to new permissions: {new_permissions}')

        if not self.database_support.check_if_user_exist(user_to_change_permission):
            return server_response.E_USER_DOES_NOT_EXIST

        elif self.database_support.check_if_user_is_logged_in(user_to_change_permission):
            return server_response.E_USER_LOGGED_CANNOT_CHANGE_PERMISSIONS
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

        if not self.database_support.check_if_user_exist(user_to_change_status):
            return server_response.E_USER_DOES_NOT_EXIST
        elif self.database_support.check_if_user_is_logged_in(user_to_change_status):
            return server_response.E_USER_LOGGED_CANNOT_CHANGE_STATUS
        elif new_status not in ['banned', 'active']:
            return server_response.E_WRONG_STATUS
        else:
            self.database_support.data_update('users', 'status', user_to_change_status, new_status)
            return {user_to_change_status: server_response.USER_STATUS_CHANGED}

    def convert_datetime_date_to_string_date(self, date_from_db):
        converted_date = date_from_db.strftime('%Y-%m-%d')
        return converted_date

    def convert_datetime_datetime_to_string_date(self, datetime_from_db):
        if not datetime_from_db:
            return None
        else:
            converted_datetime = datetime_from_db.strftime('%Y-%m-%d')
            return converted_datetime