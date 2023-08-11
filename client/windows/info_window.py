import curses
# from base_window import BaseWindow
import cln_datas
import server_communication


class BaseWindow:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.maxY, self.maxX = self.stdscr.getmaxyx()


class InfoWindow(BaseWindow, server_communication.ServerCommunication):
    def __init__(self, stdscr, login_window):
        super().__init__(stdscr)
        self.window = self.stdscr.subwin(cln_datas.INFO_HEIGHT, cln_datas.INFO_WIDTH, 3, self.maxX - 50)
        self.window.bkgd(' ', curses.color_pair(cln_datas.COLOR_PAIR))
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
            self.window.addstr(1, 9, " " * (cln_datas.INFO_WIDTH - 14))

            command = {self.login_window.login_username: "info"}
            srv_resp = self.send_command(command)
            self.window.addstr(1, 2, f'Version: {srv_resp["version"]}')
            self.window.addstr(2, 10, " " * (cln_datas.INFO_WIDTH - 14))

            self.window.addstr(2, 2, f'Start at: {srv_resp["start_at"]}')
            self.window.addstr(3, 9, " " * (cln_datas.INFO_WIDTH - 14))

            command = {self.login_window.login_username: "uptime"}
            self.window.addstr(3, 2, f'Uptime: {self.send_command(command)["uptime"]}')
            self.window.addstr(4, 9, " " * (cln_datas.INFO_WIDTH - 14))
            self.window.addstr(4, 1, f' Logged: {self.login_window.login_username}')
            self.window.addstr(5, 13, " " * (cln_datas.INFO_WIDTH - 14))
            self.window.addstr(5, 1, f' Permissions: {self.login_window.login_permissions}')
            self.window.addstr(6, 12, " " * (cln_datas.INFO_WIDTH - 14))
            self.window.refresh()

            command = {self.login_window.login_username: {"msg_count": ""}}
            server_response = self.send_command(command)

            if "Error" in server_response:
                inbox_msg_count = server_response['Error']
                self.window.addstr(6, 1, f' Inbox msgs: {inbox_msg_count}')
                self.window.attron(curses.color_pair(cln_datas.ERROR_COLOR_PAIR))
                self.window.addstr(6, 13, f' {inbox_msg_count}')
                self.window.attroff(curses.color_pair(cln_datas.ERROR_COLOR_PAIR))
                self.window.refresh()
            else:
                inbox_msg_count = server_response["msg-inbox-count"]
                self.window.addstr(6, 1, f' Inbox msgs: {inbox_msg_count}')
                self.window.refresh()
