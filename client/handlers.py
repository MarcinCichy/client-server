import curses
import client_data


class Handlers:
    def __init__(self, window_instance):
        self.window = window_instance

    @staticmethod
    def command_handler(command, user_name):
        precommand = command.split()
        if len(precommand) == 0:
            command_type = None
        else:
            command_type = precommand[0]

        if command_type in ("user-del", "msg-del", "msg-show"):
            if len(precommand) >= 2:
                command = {command_type: precommand[1]}
            else:
                command = {command_type: None}
        elif command_type == "user-info":
            if len(precommand) >= 2:
                command = {command_type: precommand[1]}
            else:
                # This is needed, because in "menu.py" if admin permissions are set and data is None,
                # then command is send without data. So any data is needed.
                command = {command_type: "_"}
        elif command_type in ("user-perm", "user-stat"):
            if len(precommand) >= 3:
                command = {command_type: {precommand[1]: precommand[2]}}
            elif len(precommand) >= 2:
                command = {command_type: {precommand[1]: None}}
            else:
                command = {command_type: {None: None}}
        elif len(precommand) == 1:
            command_type = precommand[0]
            command = command_type
        command = {user_name: command}
        return command

    def server_response_handler(self, server_response):
        if "Error" in server_response:
            self.window.clear_previous_messages()
            self.window.attron(curses.color_pair(client_data.ERROR_COLOR_PAIR))
            self.window.show_sign_by_sign(server_response)
            self.window.attroff(curses.color_pair(client_data.ERROR_COLOR_PAIR))
            self.window.refresh()
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
        elif "Clear" in server_response:
            self.window.clear_previous_messages()
        else:
            self.window.clear_previous_messages()
            self.window.show_sign_by_sign(server_response)




