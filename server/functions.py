import json
from datetime import datetime
from os import name, system

import server_data
import server_response


class SystemUtilities:
    @staticmethod
    def clear_screen():
        """Clear the screen in depends on operating system
        (Windows, Linux or iOS)."""

        if name == "nt":
            _ = system("cls")
        else:
            _ = system("clear")

    @staticmethod
    def uptime():
        now = datetime.now()
        live_time = now - server_data.START_TIME
        return json.dumps({"uptime": str(live_time).split(".")[0]})

    @staticmethod
    def info():
        return json.dumps({"version": server_data.VERSION, "start_at": str(server_data.DATE)})

    @staticmethod
    def help(permissions):
        user_help_dict = {
            "uptime": "returns the server's live time",
            "info": "returns the version number of the server and the date it was created",
            "help": "returns the list of available commands with short description",
            "logout": "to log out the User",
            "clear": " to clear the screen",
            "msg-list": "to show content of inbox",
            "msg-snd": " to create and send message",
            "msg-del [number of message]": "to delete selected message",
            "msg-show [number of message]": "to show details of message (from, date, content)"
        }
        user_help_dict_line = {
            "line": ""
        }
        admin_help_dict = {
            "stop": "stops both the server and the client",
            "user-add": "create an account",
            "user-list": "shows the list of existing accounts",
            "user-del [username]": "deletes the selected account",
            "user-perm [username] [permission]": "change permissions [user] or [admin]",
            "user-stat [username] [status]": "change user status [active] or [banned]",
            "user-info [username]": "to show information about account of selected user"
        }

        if "user" in permissions:
            help_json = json.dumps(user_help_dict)
        elif "admin" in permissions:
            help_dict = {**user_help_dict, **user_help_dict_line, **admin_help_dict}
            help_json = json.dumps(help_dict)
        else:
            help_json = json.dumps(server_response.E_WRONG_PERMISSIONS)

        return help_json

    @staticmethod
    def unrecognised_command():
        return json.dumps(server_response.UNRECOGNISED_COMMAND)

    @staticmethod
    def stop():
        return json.dumps(server_response.CONNECTION_CLOSE)

    @staticmethod
    def clear():
        return json.dumps({"Clear": ""})
