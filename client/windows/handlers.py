import curses
import client_data


class Handlers:
    def __init__(self, window_instance, logged_in_user_data):
        self.window = window_instance
        self.logged_in_user_data = logged_in_user_data

    @staticmethod
    def command_handler(user_name, command):  # , permissions
        precommand = command.split()

        if not precommand:
            return {user_name: None}

        command_type = precommand[0]
        command_data = None

        if command_type in ("user-del", "msg-del", "msg-show"):
            command_data = {command_type: precommand[1] if len(precommand) >= 2 else None}
        elif command_type == "user-info":
            command_data = {command_type: precommand[1] if len(precommand) >= 2 else "_"}
        elif command_type in ("user-perm", "user-stat"):
            if len(precommand) >= 3:
                command_data = {command_type: {precommand[1]: precommand[2]}}
            elif len(precommand) >= 2:
                command_data = {command_type: {precommand[1]: None}}
            else:
                command_data = {command_type: {None: None}}
        elif len(precommand) == 1:
            command_data = command_type

        return {user_name: command_data}

    def server_response_handler(self, server_response):
        if "Error" in server_response:
            self.window.clear_previous_messages()
            self.window.window.attron(curses.color_pair(client_data.ERROR_COLOR_PAIR))
            self.window.show_sign_by_sign(server_response)
            self.window.window.attroff(curses.color_pair(client_data.ERROR_COLOR_PAIR))
            self.window.window.refresh()
        elif "User-add" in server_response:
            self.window.clear_previous_messages()
            self.window.useradd_window.init_window()
            self.window.useradd_window.show()
            self.window.init_window()
        elif "Msg-snd" in server_response:
            self.window.clear_previous_messages()
            self.window.new_message_window.init_window()
            self.window.new_message_window.show()
            self.window.init_window()
        elif "Message to show" in server_response:
            self.window.clear_previous_messages()
            self.window.show_message_window.init_window()
            self.window.show_message_window.show_selected_message(server_response)
            self.window.init_window()
        elif "Logout" in server_response:
            self.window.login_window.logged_in = False
            self.window.login_window.logged_username = ''
            self.logged_in_user_data.clear_user_data()
            self.logged_in_user_data.clear_user_data()
        elif "Clear" in server_response:
            self.window.clear_previous_messages()
        else:
            self.window.clear_previous_messages()
            self.window.show_sign_by_sign(server_response)

    def login_handler(self, server_response):
        if "Error" in server_response:
            self.window.window.attron(curses.color_pair(client_data.ERROR_COLOR_PAIR))
            self.window.window.addstr(4, 2, server_response['Error'])
            self.window.window.clrtoeol()
            self.window.window.attroff(curses.color_pair(client_data.ERROR_COLOR_PAIR))
            self.window.window.refresh()

        elif 'Login' in server_response:
            if server_response['Login'] == "OK":
                self.window.logged_in = True
                self.window.login_username = server_response['login_username']
                self.window.login_permissions = server_response['user_permissions']
                self.logged_in_user_data.set_user_data(self.window.login_username, self.window.login_permissions)
                self.window.window.refresh()



