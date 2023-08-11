import curses
# from base_window import BaseWindow
import cln_datas


class BaseWindow:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.maxY, self.maxX = self.stdscr.getmaxyx()


class HeaderWindow(BaseWindow):
    def __init__(self, stdscr):
        super().__init__(stdscr)
        self.window = self.stdscr.subwin(cln_datas.HEADER_HEIGHT, self.maxX, 0, 0)
        self.window.bkgd(' ', curses.color_pair(cln_datas.COLOR_PAIR))

    def init_window(self):
        self.window.border()
        self.window.addstr(1, int(self.maxX // 2) - int(len(cln_datas.CONSOLE_TITLE) // 2), cln_datas.CONSOLE_TITLE)
        self.window.refresh()


