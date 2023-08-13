import curses

import client_data
import server_communication

from .base_window import BaseWindow


class LoginWindow(BaseWindow, server_communication.ServerCommunication):
    def __init__(self, stdscr, middle_window):
        super().__init__(stdscr)
        self.window = self.stdscr.subwin(client_data.LOGIN_HEIGHT, client_data.LOGIN_WIDTH, self.maxY // 4, self.maxX // 4)
        self.window.bkgd(' ', curses.color_pair(client_data.COLOR_PAIR))
        self.username = ''
        self.password = ''
        self.command = ''
        self.login_username = ''
        self.login_permissions = ''
        self.logged_in = False
        self.middle_window = middle_window

    def init_window(self):
        self.window.border()
        self.window.addstr(1, 2, "Username: ")
        self.window.addstr(2, 2, "Password: ")
        self.window.refresh()

    def get_and_mask_password(self):
        password = ""
        start_column_pos = 12
        while True:
            character = self.window.getch(2, start_column_pos)
            if character == curses.KEY_ENTER or character == 10 or character == 13:
                break
            elif character == curses.KEY_BACKSPACE or character == ord('\b') or character == ord('\x7f'):
                if len(password) > 0:
                    password = password[:-1]
                    start_column_pos -= 1
                    self.window.move(2, start_column_pos)
                    self.window.addstr(" ")
                    self.window.refresh()
            else:
                password += chr(character)
                self.window.addstr(2, start_column_pos, "*")
                start_column_pos += 1
                self.window.refresh()
        return password

    def get_credentials(self):
        curses.curs_set(2)
        curses.echo()
        self.window.addstr(1, 12, " " * (client_data.LOGIN_WIDTH - 14))  # to clear the line after wrong logging
        self.window.addstr(2, 12, " " * (client_data.LOGIN_WIDTH - 14))  # to clear the line after wrong logging
        self.username = self.window.getstr(1, 12).decode(errors="ignore")
        self.init_window()
        self.password = self.get_and_mask_password()
        self.window.refresh()
        curses.noecho()

    def login(self):
        self.command = {
            self.username: {
                "login":
                    (
                        {'username': self.username},
                        {'password': self.password}
                    )
                }
        }
        server_response = self.send_command(self.command)

        if "Error" in server_response:
            self.window.attron(curses.color_pair(client_data.ERROR_COLOR_PAIR))
            self.window.addstr(4, 2, server_response['Error'])
            self.window.clrtoeol()
            self.window.attroff(curses.color_pair(client_data.ERROR_COLOR_PAIR))
            self.window.refresh()

        elif 'Login' in server_response:
            if server_response['Login'] == "OK":
                self.logged_in = True
                self.login_username = server_response['login_username']
                self.login_permissions = server_response['user_permissions']
                self.window.refresh()

    def show(self):
        while not self.logged_in:
            self.init_window()
            self.get_credentials()
            self.login()
