import curses

import client_data
from windows.bottom_window import BottomWindow
from windows.header_window import HeaderWindow
from windows.info_window import InfoWindow
from windows.login_window import LoginWindow
from windows.middle_window import MiddleWindow
from windows.new_message_window import NewMessageWindow
from windows.show_message_window import ShowMessageWindow
from windows.user_add_window import UserAddWindow
from windows.user_state import UserState
from windows.handlers import Handlers

class Console:
    def __init__(self, stdscr):
        self.middle_window = None
        self.stdscr = stdscr

        self.logged_in_user_data = UserState()

        # Instantiate window subclasses
        self.login_window = LoginWindow(stdscr, self.middle_window)
        self.header_window = HeaderWindow(stdscr)
        self.info_window = InfoWindow(stdscr, self.login_window, self.logged_in_user_data)
        self.bottom_window = BottomWindow(stdscr, self.logged_in_user_data)  #  self.login_window,
        self.useradd_window = UserAddWindow(stdscr, self.middle_window, self.login_window, self.logged_in_user_data)
        self.new_message_window = NewMessageWindow(stdscr, self.middle_window, self.login_window, self.logged_in_user_data)
        self.show_message_window = ShowMessageWindow(stdscr)
        self.middle_window = MiddleWindow(stdscr, self.bottom_window, self.useradd_window, self.new_message_window, self.show_message_window, self.login_window, self.logged_in_user_data)
        self.init_curses()

    def init_curses(self):
        curses.start_color()
        curses.init_pair(client_data.COLOR_PAIR, client_data.COLOR_FG, client_data.COLOR_BG)
        curses.init_pair(client_data.ERROR_COLOR_PAIR, client_data.ERROR_COLOR_FG, client_data.ERROR_COLOR_BG)
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        self.stdscr.keypad(1)
        self.stdscr.nodelay(1)
        self.stdscr.attron(curses.color_pair(client_data.COLOR_PAIR))
        self.stdscr.border()
        self.stdscr.refresh()

    def start(self):
        while True:
            if not self.login_window.logged_in:
                self.hide_windows()
                self.reset()
                self.login_window.show()
            else:
                self.init_windows()
                self.useradd_window.middle_window = self.middle_window
                self.new_message_window.middle_window = self.middle_window
                self.show_message_window.middle_window = self.middle_window
                self.run()

    def init_windows(self):
        self.reset()

        self.header_window.init_window()
        self.middle_window.init_window()
        self.info_window.init_window()
        self.bottom_window.init_window()

    def reset(self):
        """
            Reset the console to its initial state. Clear the screen
        """
        self.stdscr.clear()
        self.stdscr.border()
        self.stdscr.refresh()

    def run(self):
        while self.login_window.logged_in:
            self.info_window.show_server_info()

            if self.login_window.logged_in:
                self.middle_window.send_receive_command_and_show_respond(self.bottom_window.get_command())

    def hide_windows(self):
        self.header_window.window.erase()
        self.middle_window.window.erase()
        self.info_window.window.erase()
        self.bottom_window.window.erase()
        self.useradd_window.window.erase()
        self.new_message_window.window.erase()
        self.show_message_window.window.erase()

        self.header_window.window.refresh()
        self.middle_window.window.refresh()
        self.info_window.window.refresh()
        self.bottom_window.window.refresh()
        self.useradd_window.window.refresh()
        self.new_message_window.window.refresh()
        self.show_message_window.window.refresh()


def main(stdscr):
    console = Console(stdscr)
    console.start()


if __name__ == '__main__':
    curses.wrapper(main)
