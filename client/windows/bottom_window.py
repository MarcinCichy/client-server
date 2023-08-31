import curses

import client_data

from .base_window import BaseWindow
from .handlers import Handlers


class BottomWindow(BaseWindow):
    def __init__(self, stdscr, logged_in_user_data):
        super().__init__(stdscr)
        self.window = self.stdscr.subwin(client_data.BOTTOM_HEIGHT, self.maxX - 1, self.maxY - 3, 0)
        self.window.bkgd(' ', curses.color_pair(client_data.COLOR_PAIR))
        self.command = ''
        self.logged_in_user_data = logged_in_user_data

    def init_window(self):
        self.window.hline(0, 1, 0, self.maxX)
        self.window.addstr(1, 2, client_data.PROMPT)
        self.window.refresh()

    def get_command(self):
        curses.curs_set(2)
        curses.echo()
        command = self.window.getstr().decode(errors="ignore")

        username = self.logged_in_user_data.logged_in_username
        permissions = self.logged_in_user_data.logged_in_permissions
        command_to_server = Handlers.command_handler(username, permissions, command)

        self.window.move(1, 19)
        self.window.clrtoeol()
        return command_to_server
