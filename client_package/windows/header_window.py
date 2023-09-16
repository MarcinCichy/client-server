import curses
import client_package.client_data as client_data
from .base_window import BaseWindow


class HeaderWindow(BaseWindow):
    def __init__(self, stdscr):
        super().__init__(stdscr)
        self.window = self.stdscr.subwin(client_data.HEADER_HEIGHT, self.maxX, 0, 0)
        self.window.bkgd(' ', curses.color_pair(client_data.COLOR_PAIR))

    def init_window(self):
        self.window.border()
        self.window.addstr(1, int(self.maxX // 2) - int(len(client_data.CONSOLE_TITLE) // 2), client_data.CONSOLE_TITLE)
        self.window.refresh()


