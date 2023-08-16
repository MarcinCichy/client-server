import curses
from .base_window import BaseWindow
import client_data


class ShowMessageWindow(BaseWindow):
    def __init__(self, stdscr, middle_window):
        super().__init__(stdscr)
        self.window = self.stdscr.subwin(client_data.SHOW_MSG_HEIGHT, client_data.SHOW_MSG_WIDTH, self.maxY // 4,
                                         self.maxX // 4)
        self.window.bkgd(' ', curses.color_pair(client_data.COLOR_PAIR))
        self.content = ''
        self.date = ''
        self.show_message_window = False  # sprawdzic to
        self.middle_window = middle_window
        self.sender = None
        self.maxX_SMW = self.window.getmaxyx()[1]

    def init_window(self):
        self.window.border()
        self.window.addstr(1, 2, "From: ")
        self.window.addstr(2, 2, "Date: ")
        self.window.addstr(3, 2, "Content: ")
        self.window.refresh()

    def show_selected_message(self, message_content):
        self.init_window()  # sprawdzić

        self.sender = message_content["Message to show"]["sender"]
        self.date = message_content["Message to show"]["date"]
        self.content = message_content["Message to show"]["content"]

        self.init_window()
        self.small_show_sign_by_sign(1, self.sender)
        self.window.refresh()
        self.small_show_sign_by_sign(2, self.date)
        self.window.refresh()
        self.small_show_sign_by_sign(3, self.content)
        self.window.refresh()

        curses.curs_set(0)

        while True:
            key = self.window.getch()
            if key == ord('\n'):  # Enter
                self.window.erase()
                self.window.refresh()
                break

    def small_show_sign_by_sign(self, row, text):
        column = 0
        self.window.refresh()
        for char in str(text):
            if column >= self.maxX_SMW - 14:
                row += 1
                column = 0
            self.window.addch(row, 11 + column, str(char))
            curses.delay_output(100)
            self.window.refresh()
            column += 1
