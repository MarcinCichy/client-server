import json
from datetime import datetime
from os import name, system

import srv_datas
import srv_response


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
        live_time = now - srv_datas.START_TIME
        uptime_dict = {"uptime": str(live_time).split(".")[0]}
        uptime_json = json.dumps(uptime_dict)
        return uptime_json

    @staticmethod
    def info():
        info_dict = {"version": srv_datas.VERSION, "start_at": str(srv_datas.DATE)}
        info_json = json.dumps(info_dict)
        return info_json

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
            help_json = json.dumps({})

        return help_json

    @staticmethod
    def unrecognised_command():
        un_comm_dict = srv_response.UNRECOGNISED_COMMAND
        un_comm_json = json.dumps(un_comm_dict)
        return un_comm_json

    @staticmethod
    def stop():
        stop_dict = srv_response.CONNECTION_CLOSE
        stop_json = json.dumps(stop_dict)
        return stop_json

    @staticmethod
    def clear():
        clear_dict = {"Clear": ""}
        clear_json = json.dumps(clear_dict)
        return clear_json
