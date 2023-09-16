import curses
from datetime import datetime
import client_package.client_data as client_data
from .base_window import BaseWindow
from client_package.server_communication import ServerCommunication


class NewMessageWindow(BaseWindow):
    def __init__(self, stdscr, middle_window, login_window):
        super().__init__(stdscr)
        self.window = self.stdscr.subwin(client_data.NEW_MSG_HEIGHT, client_data.NEW_MSG_WIDTH, self.maxY // 4,
                                         self.maxX // 4)
        self.window.bkgd(' ', curses.color_pair(client_data.COLOR_PAIR))
        self.recipient = ''
        self.content = ''
        self.middle_window = middle_window
        self.message_exceeded = None
        self.max_msg_length = None
        self.login_window = login_window

    def init_window(self):
        self.max_msg_length = client_data.MAX_MESSAGE_LENGTH

        self.window.border()
        self.window.refresh()
        self.window.addstr(1, 2, "Recipient: ")
        self.window.refresh()
        self.window.addstr(2, 2, "Content: ")
        self.window.refresh()
        self.window.addstr(10, client_data.NEW_MSG_WIDTH - 9, f'0/{self.max_msg_length}')
        self.window.refresh()

    def clear_line(self, y_poz):
        self.window.addstr(y_poz, 12, client_data.CLEAR_SPACE_NEW_MSG__WINDOW)

    def number_of_chars(self):
        count = len(self.content)
        if count >= 250:
            self.window.attron(curses.color_pair(client_data.ERROR_COLOR_PAIR))
        else:
            self.window.attron(curses.color_pair(client_data.COLOR_PAIR))
        self.window.addstr(10, client_data.NEW_MSG_WIDTH - 9, f'{count}/{self.max_msg_length} ')
        self.window.refresh()

    def get_new_message(self):
        username = self.login_window.logged_username

        self.content = ''
        # command = {}
        self.window.attron(curses.color_pair(client_data.COLOR_PAIR))
        curses.curs_set(2)
        curses.echo()
        self.window.refresh()
        self.clear_line(1)
        self.clear_line(2)

        self.recipient = self.window.getstr(1, 15).decode(errors="ignore")
        self.init_window()

        self.message_exceeded = False

        content_y, content_x = 2, 15
        self.window.move(content_y, content_x)

        while True:
            key = self.window.getch()
            if key == 10:  # Enter
                break
            content_y, content_x = self.handle_key(key, content_y, content_x)

        command = self.build_command(username)
        self.window.erase()
        self.window.refresh()
        curses.noecho()

        server_response = ServerCommunication.send_command(command)
        self.middle_window.show_response(server_response)

    def handle_key(self, key, content_y, content_x):
        if key == curses.KEY_BACKSPACE or key == ord('\b') or key == ord('\x7f'):
            content_y, content_x = self.handle_backspace(content_y, content_x)
        elif key in [curses.KEY_LEFT, curses.KEY_RIGHT, curses.KEY_UP, curses.KEY_DOWN]:
            content_y, content_x = self.handle_arrow_keys(key, content_y, content_x)
        elif key == curses.KEY_DC:
            content_y, content_x = self.handle_delete(content_y, content_x)
        else:
            content_y, content_x = self.handle_char_input(key, content_y, content_x)
        return content_y, content_x

    def handle_backspace(self, content_y, content_x):
        if content_x > 15:
            content_x -= 1
            self.content = self.content[:-1]
            self.window.delch(content_y, content_x)
            self.window.insstr(content_y, client_data.NEW_MSG_WIDTH - 2, " ")
            if content_x < client_data.NEW_MSG_WIDTH - 2:
                self.window.move(content_y, content_x)
            self.message_exceeded = False
            self.number_of_chars()
            self.window.move(content_y, content_x)
            self.window.attron(curses.color_pair(client_data.COLOR_PAIR))
        else:
            if content_y > 2:
                content_y -= 1
                content_x = len(self.content) % (client_data.NEW_MSG_WIDTH - 15) + 15
                self.window.move(content_y, content_x)
                self.message_exceeded = False
        return content_y, content_x

    def handle_arrow_keys(self, key, content_y, content_x):
        if key == curses.KEY_LEFT:
            if content_x > 15:
                content_x -= 1
                self.window.move(content_y, content_x)
        elif key == curses.KEY_RIGHT:
            if content_x < client_data.NEW_MSG_WIDTH - 2:
                content_x += 1
                self.window.move(content_y, content_x)
        elif key == curses.KEY_UP:
            if content_y > 2:
                content_y -= 1
                self.window.move(content_y, content_x)
        elif key == curses.KEY_DOWN:
            if content_y < client_data.NEW_MSG_HEIGHT - 2:
                content_y += 1
                self.window.move(content_y, content_x)
        return content_y, content_x

    def handle_delete(self, content_y, content_x):
        if content_x < client_data.NEW_MSG_WIDTH - 2:
            self.content = self.content[:content_x - 15] + self.content[content_x - 14:]
            self.window.delch(content_y, content_x)
            self.window.insstr(content_y, client_data.NEW_MSG_WIDTH - 2, " ")
            if content_x < client_data.NEW_MSG_WIDTH - 2:
                self.window.move(content_y, content_x)
            self.message_exceeded = False
            self.number_of_chars()
        self.window.move(content_y, content_x)
        return content_y, content_x

    def handle_char_input(self, key, content_y, content_x):
        char = chr(key)
        if char.isprintable() and len(self.content) < self.max_msg_length:
            if content_x == client_data.NEW_MSG_WIDTH - 3:
                if content_y < client_data.NEW_MSG_HEIGHT - 1:
                    content_y += 1
                    content_x = 15
            self.content += char
            if len(self.content) >= self.max_msg_length:
                self.window.move(content_y, content_x)
            self.window.addch(content_y, content_x, char)
            content_x += 1
            curses.noecho()
        self.number_of_chars()
        self.window.move(content_y, content_x)
        self.window.attron(curses.color_pair(client_data.COLOR_PAIR))
        if len(self.content) >= self.max_msg_length:
            self.message_exceeded = True
        else:
            self.message_exceeded = False
        return content_y, content_x

    def build_command(self, username):
        date = datetime.now().strftime("%Y-%m-%d")
        command = {
            username: {
                "new_message": (
                    {'sender': username},
                    {'date': str(date)},
                    {'recipient': self.recipient},
                    {'content': self.content}
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

        self.get_new_message()
        curses.noecho()
        curses.curs_set(0)
        self.window.keypad(0)
        self.window.timeout(100)
