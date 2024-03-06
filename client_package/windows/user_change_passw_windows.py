import curses
import client_package.client_data as client_data
from .base_window import BaseWindow
from client_package.client_communication import ClientCommunication


class UserChangePasswWindow(BaseWindow):
    def __init__(self, stdscr, middle_window, login_window):
        super().__init__(stdscr)
        self.window = self.stdscr.subwin(client_data.CHANGE_PASSWD_HEIGHT, client_data.CHANGE_PASSWD_WIDTH, self.maxY // 4,
                                         self.maxX // 4)
        self.window.bkgd(' ', curses.color_pair(client_data.COLOR_PAIR))
        self.username = ''
        self.new_password = ''
        self.confirm_new_password = ''
        self.middle_window = middle_window
        self.login_window = login_window

    def init_window(self):
        self.window.border()
        self.window.addstr(1, 2, "Username: ")
        self.window.addstr(2, 2, "New Password: ")
        self.window.addstr(3, 2, "Confirm New Password: ")
        self.window.refresh()

    def clear_line(self, y_poz):
        self.window.addstr(y_poz, 24, client_data.CLEAR_SPACE_CHANGE_PASSWD_WINDOW)

    def get_change_password_data(self):
        logged_username = self.login_window.logged_username
        curses.curs_set(2)
        curses.echo()
        self.window.refresh()
        self.clear_line(1)
        self.clear_line(2)
        self.clear_line(3)
        self.username = self.window.getstr(1, 12).decode(errors="ignore")
        self.init_window()  # this line is needed to preserve window borders at right side
        self.new_password = self.window.getstr(2, 16).decode(errors="ignore")
        self.init_window()  # this line is needed to preserve window borders at right side
        self.confirm_new_password = self.window.getstr(3, 24).decode(errors="ignore")

        command = self.build_command(logged_username)
        self.window.erase()
        self.window.refresh()
        curses.noecho()

        server_response = ClientCommunication.send_command(command)
        self.middle_window.show_response(server_response)

    def build_command(self, logged_username):

        command = {
            logged_username: {
                    "change_password": (
                        {'username': self.username},
                        {'new_password': self.new_password},
                        {'confirm_new_password': self.confirm_new_password}
                    )
                }
        }
        return command

    def show(self):
        self.init_window()
        self.window.keypad(1)
        self.window.timeout(-1)
        curses.curs_set(2)
        curses.echo()

        self.init_window()
        self.get_change_password_data()

        curses.noecho()
        curses.curs_set(0)
        self.window.keypad(0)
        self.window.timeout(100)
