import curses
from datetime import datetime
import client_data
from .base_window import BaseWindow


class UserAddWindow(BaseWindow):
    def __init__(self, stdscr, middle_window, login_window):
        super().__init__(stdscr)
        self.window = self.stdscr.subwin(client_data.ADDUSER_HEIGHT, client_data.ADDUSER_WIDTH, self.maxY // 4,
                                         self.maxX // 4)
        self.window.bkgd(' ', curses.color_pair(client_data.COLOR_PAIR))
        self.new_username = ''
        self.new_password = ''
        self.new_permissions = ''
        self.command = ''
        self.middle_window = middle_window
        self.activation_date = datetime.now().strftime("%Y-%m-%d")
        self.login_window = login_window

    def init_window(self):
        self.window.border()
        self.window.addstr(1, 2, "Username: ")
        self.window.addstr(2, 2, "Password: ")
        self.window.addstr(3, 2, "Permissions: ")
        self.window.refresh()

    def clear_line(self, y_poz):
        self.window.addstr(y_poz, 12, client_data.CLEAR_SPACE_ADDUSER_WINDOW)

    def get_new_account_data(self):
        logged_username = self.login_window.logged_username
        curses.curs_set(2)
        curses.echo()
        self.window.refresh()
        self.clear_line(1)
        self.clear_line(2)
        self.clear_line(3)
        self.new_username = self.window.getstr(1, 15).decode(errors="ignore")
        self.init_window()  # this line is needed to preserve window borders at right side
        self.new_password = self.window.getstr(2, 15).decode(errors="ignore")
        self.init_window()  # this line is needed to preserve window borders at right side
        self.new_permissions = self.window.getstr(3, 15).decode(errors="ignore")

        self.command = {
            logged_username:
                {
                    "create_account": (
                        {'username': self.new_username},
                        {'password': self.new_password},
                        {'permissions': self.new_permissions},
                        {'status': "active"},
                        {'activation_date': self.activation_date}
                    )
                }
        }

        self.window.erase()
        self.window.refresh()
        curses.noecho()

        self.middle_window.send_receive_command_and_show_response(self.command)

    def show(self):
        self.init_window()
        self.window.keypad(1)
        self.window.timeout(-1)
        curses.curs_set(2)
        curses.echo()

        self.init_window()
        self.get_new_account_data()

        curses.noecho()
        curses.curs_set(0)
        self.window.keypad(0)
        self.window.timeout(100)


