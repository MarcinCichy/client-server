import curses
import client_package.client_data as client_data
from client_package.client_communication import ClientCommunication
from .base_window import BaseWindow


class InfoWindow(BaseWindow):
    def __init__(self, stdscr, login_window):
        super().__init__(stdscr)
        self.window = self.stdscr.subwin(client_data.INFO_HEIGHT, client_data.INFO_WIDTH, 3, self.maxX - 50)
        self.window.bkgd(' ', curses.color_pair(client_data.COLOR_PAIR))
        self.login_window = login_window

    def init_window(self):
        self.window.border()

    def clear_line(self, y_poz):
        self.window.addstr(y_poz, 10, client_data.CLEAR_SPACE_INFO_WINDOW)

    def show_server_info(self):
        username = self.login_window.logged_username
        permissions = self.login_window.logged_user_permissions

        command = {username: ""}
        check_connection = ClientCommunication.send_command(command)
        if "Error" not in check_connection.keys():
            self.window.refresh()

            self.clear_line(1)
            command = {username: "info"}
            server_response = ClientCommunication.send_command(command)
            self.window.addstr(1, 2, f'Version: {server_response["version"]}')

            self.clear_line(2)
            self.window.addstr(2, 2, f'Start at: {server_response["start_at"]}')

            self.clear_line(3)
            command = {username: "uptime"}
            self.window.addstr(3, 2, f'Uptime: {ClientCommunication.send_command(command)["uptime"]}')

            self.clear_line(4)
            self.window.addstr(4, 1, f' Logged: {username}')

            self.clear_line(5)
            self.window.addstr(5, 1, f' Permissions: {permissions}')

            self.clear_line(6)
            self.window.refresh()

            command = {username: {"msg_count": ""}}
            server_response = ClientCommunication.send_command(command)

            if "Error" in server_response:
                inbox_msg_count = server_response['Error']
                self.window.addstr(6, 1, f' Inbox msgs: {inbox_msg_count}')
                self.window.attron(curses.color_pair(client_data.ERROR_COLOR_PAIR))
                self.window.addstr(6, 13, f' {inbox_msg_count}')
                self.window.attroff(curses.color_pair(client_data.ERROR_COLOR_PAIR))
                self.window.refresh()
            else:
                inbox_msg_count = server_response["msg-inbox-count"]
                self.window.addstr(6, 1, f' Inbox msgs: {inbox_msg_count}')
                self.window.refresh()
