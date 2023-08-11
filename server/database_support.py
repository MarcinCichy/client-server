import json
import srv_response
from functools import wraps


def handle_db_file_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            return srv_response.E_FILE_IS_UNAVAILABLE
    return wrapper


class DatabaseSupport:
    @staticmethod
    def read_db_json(db_file):
        try:
            with open(db_file, 'r') as file:
                db = json.load(file)
            return db
        except FileNotFoundError:
            print(f'{srv_response.E_UNABLE_TO_OPEN_DB_FILE} - {db_file}')
            raise Exception(srv_response.E_UNABLE_TO_OPEN_DB_FILE)

    @staticmethod
    def save_db_json(db, db_file):
        try:
            with open(db_file, 'w') as file:
                json.dump(db, file, indent=4)
        except FileNotFoundError:
            print(f'{srv_response.E_UNABLE_TO_SAVE_DB_FILE} - {db_file}')
            raise Exception(srv_response.E_UNABLE_TO_SAVE_DB_FILE)

