import json
from database_support import DatabaseSupport
from functions import SystemUtilities
from message_management import MessageManagement
from user_management import UserManagement
from user_authentication import UserAuthentication
import server_response


class CommandHandler:
    def __init__(self, database_support):
        self.username = ""
        self.comm = ""
        self.permissions = ""
        self.database_support = database_support
        self.user_auth = UserAuthentication(self.database_support)
        self.permissions = self.user_auth.get_permissions(self.username)
        self.user_management = UserManagement(self.database_support)
        self.message_management = MessageManagement(self.database_support)

        self.all_users_commands = {
            "login": self.user_auth.login,
            "logout": self.user_auth.logout,
            "help": SystemUtilities.help,
            "info": SystemUtilities.info,
            "uptime": SystemUtilities.uptime,
            "clear": SystemUtilities.clear,
            "msg_count": self.message_management.msg_count,
            "msg-list": self.message_management.msg_list,
            "msg-snd": self.message_management.msg_snd,
            "msg-del": self.message_management.msg_del,
            "new_message": self.message_management.new_message,
            "msg-show": self.message_management.msg_show
        }
        self.admin_commands = {
            "stop": SystemUtilities.stop,
            "user-add": self.user_management.user_add,
            "user-list": self.user_management.user_list,
            "user-del": self.user_management.user_del,
            "user-perm": self.user_management.user_perm,
            "user-stat": self.user_management.user_stat,
            "user-info": self.user_management.user_info,
            "create_account": self.user_management.create_account
        }

    def use_command(self, entrance_comm):
        if isinstance(entrance_comm, dict):
            # Extract the first key, which is the username submitted
            self.username = next(iter(entrance_comm))
            # Based on this username, create a new dictionary with the command
            self.comm = entrance_comm.pop(self.username)
            self.permissions = self.user_auth.get_permissions(self.username)
            print(f'NEW_COMMAND  = {self.comm}')
            print(f'ENTRANCE USERNAME = {self.username}')
            print(f'ENTRANCE PERMISSIONS: {self.permissions}')

        if isinstance(self.comm, dict):
            print(f'REAL COMMAND = {list(self.comm.keys())[0]}')
            command = list(self.comm.keys())[0]
            data = self.comm[command]
        else:
            command = self.comm
            data = None

#  --------------------------------------------------------------------------------------
        if command in self.all_users_commands:
            match command:
                case "login":
                    self.username = data[0]['username']
                    self.permissions = self.user_auth.get_permissions(self.username)
                case "logout":
                    data = self.username
                    self.username = None
                    self.permissions = None
                case "help":
                    data = self.permissions
                case "msg-list":
                    data = self.username
                case "msg-del":
                    data = {self.username: data}
                case "msg-show":
                    data = {self.username: data}
                case "msg_count":
                    data = self.username
                case _:
                    pass

            if data is not None:
                result = self.all_users_commands[command](data)
            else:
                result = self.all_users_commands[command]()

        elif command in self.admin_commands:
            if self.permissions == "admin":
                if data is not None:
                    result = self.admin_commands[command](data)
                else:
                    result = self.admin_commands[command]()
            else:
                result = server_response.E_COMMAND_UNAVAILABLE
        else:
            result = SystemUtilities.unrecognised_command()

        print(f'Server response: {result}')
        print(f'EXIT USERNAME = {self.username}')
        print(f'EXIT PERMISSIONS: {self.permissions}')
        print(f'EXIT DATA = {data}')
        if isinstance(result, dict):
            return json.dumps(result)
        else:
            return result


database_support = DatabaseSupport()
handler = CommandHandler(database_support)
