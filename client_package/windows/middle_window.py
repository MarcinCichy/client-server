import curses
import client_package.client_data as client_data
from .base_window import BaseWindow
from .handlers import Handlers


class MiddleWindow(BaseWindow):
    def __init__(self, stdscr, useradd_window, new_message_window, show_message_window, login_window):
        super().__init__(stdscr)
        self.window = self.stdscr.subwin(self.maxY - 5, client_data.MIDDLE_HEIGHT, 2, 1)
        self.window.bkgd(' ', curses.color_pair(client_data.COLOR_PAIR))
        self.previous_message = ''
        self.command = ''
        self.useradd_window = useradd_window
        self.new_message_window = new_message_window
        self.show_message_window = show_message_window
        self.maxY = self.window.getmaxyx()[0]
        self.maxX = self.window.getmaxyx()[1]
        self.console = None
        self.handler = Handlers(self)
        self.login_window = login_window

    def init_window(self):
        self.window.addstr(1, 2, "Server response: ")
        self.window.refresh()

    def clear_previous_messages(self):
        """
                Used to clear a message before displaying a new one.
        """
        for num_of_row in range(self.maxY - client_data.START_POINT - 1):
            self.window.move(client_data.START_POINT + num_of_row, 10)
            self.window.clrtoeol()
            self.window.refresh()

    def show_character_by_character(self, sentence):
        """
                To show answer from server_package in terminal.
                The answer is displayed letter by letter like in old terminals ;-)
        """
        self.clear_previous_messages()
        row = 0
        column = 0
        self.window.refresh()
        if "msg" in sentence.keys():
            sentence = sentence['msg']
            self.window.addstr(2, 10, "Messages: ")
            self.window.hline(client_data.START_POINT + 1, 10, 0, 30)
            row = 2
        elif "Existing_accounts" in sentence.keys():
            sentence = sentence['Existing_accounts']
            self.window.addstr(2, 10, "Existing accounts: ")
            self.window.hline(client_data.START_POINT + 1, 10, 0, 30)
            row = 2
        elif "Account_info" in sentence.keys():
            sentence = sentence['Account_info']
            self.window.addstr(2, 10, "Account info: ")
            self.window.hline(client_data.START_POINT + 1, 10, 0, 30)
            row = 2

        for response_keyword, response_content in sentence.items():
            if response_content == "line":
                self.window.hline(client_data.START_POINT + row, 10, 0, self.maxX)
                row += 1
            else:
                text = f"{response_keyword} : {response_content}"
                self.window.refresh()
                for char in str(text):
                    if column == self.maxX - 3:
                        row += 1
                        column = 0
                    if char not in '{}':
                        self.window.addch(client_data.START_POINT + row, 10 + column, str(char))
                    curses.delay_output(100)
                    self.window.refresh()
                    column += 1
                row += 1
                column = 0

    def show_response(self, server_response):
        self.handler.server_response_handler(server_response)
        self.previous_message = server_response

