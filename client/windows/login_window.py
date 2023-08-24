import curses

import client_data
from server_communication import ServerCommunication
from .base_window import BaseWindow
from .handlers import Handlers

class LoginWindow(BaseWindow):
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
        self.handler = Handlers(self)

    def init_window(self):
        self.window.border()
        self.window.addstr(1, 2, "Username: ")
        self.window.addstr(2, 2, "Password: ")
        self.window.refresh()

    def clear_line(self, y_pos):
        self.window.addstr(y_pos, 10, client_data.CLEAR_SPACE_LOGIN_WINDOW)

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
        self.clear_line(1)
        self.clear_line(2)
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
        server_response = ServerCommunication.send_command(self.command)
        return server_response

    def show(self):
        while not self.logged_in:
            self.init_window()
            self.get_credentials()
            response = self.login()
            self.handler.login_handler(response)
