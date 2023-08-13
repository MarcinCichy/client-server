import curses

import client_data
import server_communication

from .base_window import BaseWindow


class InfoWindow(BaseWindow, server_communication.ServerCommunication):
    def __init__(self, stdscr, login_window):
        super().__init__(stdscr)
        self.window = self.stdscr.subwin(client_data.INFO_HEIGHT, client_data.INFO_WIDTH, 3, self.maxX - 50)
        self.window.bkgd(' ', curses.color_pair(client_data.COLOR_PAIR))
        self.login_window = login_window
        self.logged_username = self.login_window.login_username
        self.logged_user_permissions = self.login_window.login_permissions

    def init_window(self):
        self.window.border()

    def show_server_info(self):
        command = {"command": ""}
        check_connection = self.send_command(command)
        if "Error" not in check_connection.keys():
            self.window.refresh()
            self.window.addstr(1, 9, " " * (client_data.INFO_WIDTH - 14))

            command = {self.login_window.login_username: "info"}
            server_resp = self.send_command(command)
            self.window.addstr(1, 2, f'Version: {server_resp["version"]}')
            self.window.addstr(2, 10, " " * (client_data.INFO_WIDTH - 14))

            self.window.addstr(2, 2, f'Start at: {server_resp["start_at"]}')
            self.window.addstr(3, 9, " " * (client_data.INFO_WIDTH - 14))

            command = {self.login_window.login_username: "uptime"}
            self.window.addstr(3, 2, f'Uptime: {self.send_command(command)["uptime"]}')
            self.window.addstr(4, 9, " " * (client_data.INFO_WIDTH - 14))
            self.window.addstr(4, 1, f' Logged: {self.login_window.login_username}')
            self.window.addstr(5, 13, " " * (client_data.INFO_WIDTH - 14))
            self.window.addstr(5, 1, f' Permissions: {self.login_window.login_permissions}')
            self.window.addstr(6, 12, " " * (client_data.INFO_WIDTH - 14))
            self.window.refresh()

            command = {self.login_window.login_username: {"msg_count": ""}}
            server_response = self.send_command(command)

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
