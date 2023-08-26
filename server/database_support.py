import json
from functools import wraps

import server_response


def handle_db_file_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            return server_response.E_FILE_IS_UNAVAILABLE
            # raise Exception(server_response.E_UNABLE_TO_OPEN_DB_FILE)
    return wrapper


class DatabaseSupport:
    @staticmethod
    @handle_db_file_error
    def read_db_json(db_file):
        with open(db_file, 'r') as file:
            db = json.load(file)
        return db

    @staticmethod
    @handle_db_file_error
    def save_db_json(db, db_file):
        with open(db_file, 'w') as file:
            json.dump(db, file, indent=4)


