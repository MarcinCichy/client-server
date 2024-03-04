import curses

"""
    Data for the Client part
"""

# ----------------------------------------------------

HOST = "127.0.0.1"
PORT = 65432
BUFFER_SIZE = 1024
ENCODE_FORMAT = "utf-8"

# ----------------------------------------------------

CLOSE = "close"

# --------------- CONSOLE CONFIGURATION --------------

CONSOLE_TITLE = 'Client Server System'
PROMPT = "Enter a command: "
START_POINT = 2
MAX_MESSAGE_LENGTH = 250
LOCAL_COMMANDS = ('msg-snd', 'clear', 'user-add')


# Color scheme
COLOR_PAIR = 1
COLOR_FG = curses.COLOR_GREEN
COLOR_BG = curses.COLOR_BLACK
ERROR_COLOR_PAIR = 2
ERROR_COLOR_FG = curses.COLOR_RED
ERROR_COLOR_BG = curses.COLOR_BLACK

# Windows dimensions
HEADER_HEIGHT = 3
MIDDLE_HEIGHT = 89
BOTTOM_HEIGHT = 3
INFO_HEIGHT = 8
INFO_WIDTH = 48
LOGIN_HEIGHT = 6
LOGIN_WIDTH = 60
ADDUSER_HEIGHT = 6
ADDUSER_WIDTH = 60
CHANGE_PASSWD_HEIGHT = 6
CHANGE_PASSWD_WIDTH = 60
NEW_MSG_HEIGHT = 12
NEW_MSG_WIDTH = 50
SHOW_MSG_HEIGHT = 12
SHOW_MSG_WIDTH = 50

CLEAR_SPACE_INFO_WINDOW = " " * (INFO_WIDTH - 14)
CLEAR_SPACE_LOGIN_WINDOW = " " * (LOGIN_WIDTH - 14)
CLEAR_SPACE_ADDUSER_WINDOW = " " * (ADDUSER_WIDTH - 14)
CLEAR_SPACE_CHANGE_PASSWD_WINDOW = " " * (ADDUSER_WIDTH - 10)
CLEAR_SPACE_NEW_MSG__WINDOW = " " * (NEW_MSG_WIDTH - 24)

# ----------------------------------------------------
