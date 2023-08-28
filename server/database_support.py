import json
from functools import wraps

import server_response


def handle_db_file_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        # If a file is unreachable, it means that the key in that file is also unreachable.
        # Therefore, exceptions for no file and no key were used.
        except (FileNotFoundError, KeyError):
            return server_response.E_FILE_IS_UNAVAILABLE
    return wrapper


class DatabaseSupport:
    @staticmethod
    @handle_db_file_error
    def read_db_json(db_file):
        with open(db_file, 'r') as file:
            return json.load(file)

    @staticmethod
    @handle_db_file_error
    def save_db_json(db, db_file):
        with open(db_file, 'w') as file:
            json.dump(db, file, indent=4)


