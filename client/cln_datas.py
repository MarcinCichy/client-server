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
START_POINT = 2
MAX_MESSAGE_LENGTH = 250

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
NEW_MSG_HEIGHT = 12
NEW_MSG_WIDTH = 50
SHOW_MSG_HEIGHT = 12
SHOW_MSG_WIDTH = 50

# ----------------------------------------------------
