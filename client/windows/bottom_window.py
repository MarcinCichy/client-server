import curses
# import base_window
import cln_datas


class BaseWindow:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.maxY, self.maxX = self.stdscr.getmaxyx()


class BottomWindow(BaseWindow):
    def __init__(self, stdscr, login_window):
        super().__init__(stdscr)
        self.window = self.stdscr.subwin(cln_datas.BOTTOM_HEIGHT, self.maxX - 1, self.maxY - 3, 0)
        self.window.bkgd(' ', curses.color_pair(cln_datas.COLOR_PAIR))
        self.login_window = login_window

    def init_window(self):
        self.window.hline(0, 1, 0, self.maxX)
        self.window.addstr(1, 2, "Enter a command: ")
        self.window.refresh()

    def get_command(self):
        """
        Get input from the user
        """
        curses.curs_set(2)
        curses.echo()
        command = self.window.getstr().decode(errors="ignore")

        precommand = command.split()
        if len(precommand) == 0:
            command_type = None
        else:
            command_type = precommand[0]

        if command_type in ("user-del", "msg-del", "msg-show"):
            if len(precommand) >= 2:
                command = {command_type: precommand[1]}
            else:
                command = {command_type: None}
        elif command_type == "user-info":
            if len(precommand) >= 2:
                command = {command_type: precommand[1]}
            else:
                command = {command_type: "_"}  # this is needed, because in "menu.py" if admin permissions are set and data is None, then command is send without data
        elif command_type in ("user-perm", "user-stat"):
            if len(precommand) >= 3:
                command = {command_type: {precommand[1]: precommand[2]}}
            elif len(precommand) >= 2:
                command = {command_type: {precommand[1]: None}}
            else:
                command = {command_type: {None: None}}
        elif len(precommand) == 1:
            command_type = precommand[0]
            command = command_type
        self.window.move(1, 19)
        self.window.clrtoeol()
        command = {self.login_window.login_username: command}
        return command
