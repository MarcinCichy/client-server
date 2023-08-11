import curses
# from base_window import BaseWindow
import cln_datas
from datetime import datetime


class BaseWindow:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.maxY, self.maxX = self.stdscr.getmaxyx()


class UserAddWindow(BaseWindow):
    def __init__(self, stdscr, middle_window, login_window, console):
        super().__init__(stdscr)
        self.window = self.stdscr.subwin(cln_datas.ADDUSER_HEIGHT, cln_datas.ADDUSER_WIDTH, self.maxY // 4,
                                         self.maxX // 4)
        self.window.bkgd(' ', curses.color_pair(cln_datas.COLOR_PAIR))
        self.new_username = ''
        self.new_password = ''
        self.new_permissions = ''
        self.command = ''
        self.login_window = login_window
        self.middle_window = middle_window
        self.activation_date = datetime.now().strftime("%Y-%m-%d")
        # self.console = console
        self.useradd_window_closed = False  # sprawdzic to

    def init_window(self):
        self.window.border()
        self.window.addstr(1, 2, "Username: ")
        self.window.addstr(2, 2, "Password: ")
        self.window.addstr(3, 2, "Permissions: ")
        self.window.refresh()

    def get_new_account_data(self):
        curses.curs_set(2)
        curses.echo()
        self.window.refresh()
        self.window.addstr(1, 12, " " * (cln_datas.ADDUSER_WIDTH - 14))
        self.window.addstr(2, 12, " " * (cln_datas.ADDUSER_WIDTH - 14))
        self.window.addstr(3, 12, " " * (cln_datas.ADDUSER_WIDTH - 14))
        self.new_username = self.window.getstr(1, 15).decode(errors="ignore")
        self.init_window()
        self.new_password = self.window.getstr(2, 15).decode(errors="ignore")
        self.init_window()
        self.new_permissions = self.window.getstr(3, 15).decode(errors="ignore")
        self.command = {
            self.login_window.login_username:
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
        self.middle_window.send_command_to_server_and_receive(self.command)

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

    def close_window(self):
        self.useradd_window_closed = True

