import curses
# import base_window
import cln_datas
import server_communication


class BaseWindow:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.maxY, self.maxX = self.stdscr.getmaxyx()


class MiddleWindow(BaseWindow):
    def __init__(self, stdscr, info_window, bottom_window, useradd_window, new_message_window, show_message_window, login_window):
        super().__init__(stdscr)
        self.window = self.stdscr.subwin(self.maxY - 5, cln_datas.MIDDLE_HEIGHT, 2, 1)
        self.window.bkgd(' ', curses.color_pair(cln_datas.COLOR_PAIR))
        self.previous_message = ''
        self.command = ''
        self.bottom_window = bottom_window
        self.info_window = info_window
        self.useradd_window = useradd_window
        self.new_message_window = new_message_window
        self.show_message_window = show_message_window
        self.login_window = login_window
        self.maxY = self.window.getmaxyx()[0]
        self.maxX = self.window.getmaxyx()[1]
        self.console = None

    def init_window(self):
        self.window.addstr(1, 2, "Server response: ")
        self.window.refresh()

    def clear_previous_messages(self):
        """
                Used to clear a message before displaying a new one.
        """
        for num_of_row in range(self.maxY - cln_datas.START_POINT - 1):
            self.window.move(cln_datas.START_POINT + num_of_row, 10)
            self.window.clrtoeol()
            self.window.refresh()

    def show_sign_by_sign(self, sentence):
        """
                To show answer from server in terminal.
                The answer is displayed letter by letter like in old terminals ;-)
        """
        self.clear_previous_messages()
        row = 0
        column = 0
        self.window.refresh()
        if "msg" in sentence.keys():
            sentence = sentence['msg']
            self.window.addstr(2, 10, "Messages: ")
            self.window.hline(cln_datas.START_POINT + 1, 10, 0, 30)
            row = 2
        elif "Existing_accounts" in sentence.keys():
            sentence = sentence['Existing_accounts']
            self.window.addstr(2, 10, "Existing accounts: ")
            self.window.hline(cln_datas.START_POINT + 1, 10, 0, 30)
            row = 2
        elif "Account_info" in sentence.keys():
            sentence = sentence['Account_info']
            self.window.addstr(2, 10, "Account info: ")
            self.window.hline(cln_datas.START_POINT + 1, 10, 0, 30)
            row = 2

        for response_keyword, response_content in sentence.items():
            if response_keyword == "line":
                self.window.hline(cln_datas.START_POINT + row, 10, 0, self.maxX)
                row += 1
            else:
                text = f"{response_keyword} : {response_content}"
                self.window.refresh()
                for char in str(text):
                    if column == self.maxX - 3:
                        row += 1
                        column = 0
                    if char not in '{}':
                        self.window.addch(cln_datas.START_POINT + row, 10 + column, str(char))
                    curses.delay_output(100)
                    self.window.refresh()
                    column += 1
                row += 1
                column = 0

    def send_command_to_server_and_receive(self, command):
        server_response = server_communication.ServerCommunication.send_command(command)

        if "Error" in server_response:
            self.clear_previous_messages()
            self.window.attron(curses.color_pair(cln_datas.ERROR_COLOR_PAIR))
            self.show_sign_by_sign(server_response)
            self.window.attroff(curses.color_pair(cln_datas.ERROR_COLOR_PAIR))
            self.window.refresh()
        elif "User-add" in server_response:
            self.clear_previous_messages()
            self.useradd_window.init_window()
            self.useradd_window.show()
            self.init_window()
        elif "Msg-snd" in server_response:
            self.clear_previous_messages()
            self.new_message_window.init_window()
            self.new_message_window.show()
            self.init_window()
        elif "Message to show" in server_response:
            self.clear_previous_messages()
            self.show_message_window.init_window()
            self.show_message_window.show_selected_message(server_response)
            self.init_window()
        elif "Logout" in server_response:
            self.login_window.logged_in = False
            self.login_window.login_username = ''
        elif "Clear" in server_response:
            self.clear_previous_messages()
        else:
            self.clear_previous_messages()
            self.show_sign_by_sign(server_response)
        self.previous_message = server_response

    def get_command(self):
        return self.bottom_window.get_command()
