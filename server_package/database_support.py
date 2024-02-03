import json
from functools import wraps
import server_package.server_response as server_response
import server_package.server_data as server_data
from server_package.connect import connect
from psycopg2 import sql
from psycopg2.extras import DictCursor


"""
    do obslugi SQLa potrzebuje komend:
    - INSERT - wstawia nowe rekordy podczs dodawania uzytkownika lub wiadomosci
    - SELECT - odczytuje istniejace rekordy podczas pobierania danych o uzytkowniku lub wiadomosciach
    - UPDATE - aktualizuje dane podczas zmiany uprawnien, statusu
    - DELETE - kasuje rekordy podczas usuwania uzytkownika lub wiadomosci
"""


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


class JSONDatabaseSupport:
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

    @handle_db_file_error
    def get_user(self):
        return self.read_db_json(server_data.USERS_DATABASE)

    @handle_db_file_error
    def save_user(self, data):
        self.save_db_json(data, server_data.USERS_DATABASE)

    @handle_db_file_error
    def get_messages(self):
        return self.read_db_json(server_data.MESSAGES_DATABASE)

    @handle_db_file_error
    def save_messages(self, data):
        self.save_db_json(data, server_data.MESSAGES_DATABASE)
# ----------------------------------------------------------------------------------------------

    def data_update(self, table, column, user_name, new_value):
        cur, conn = connect()
        try:
            query = sql.SQL("UPDATE {table} SET {column} = %s WHERE user_name = %s").format(table=sql.Identifier(table), column=sql.Identifier(column))
            cur.execute(query, (new_value, user_name))
            conn.commit()
        except Exception as e:
            print(f"Error: {e}")
            conn.rollback()
        finally:
            cur.close()
            conn.close()

    def get_info_about_user(self, user_name):
        cur, conn = connect()
        try:
            cur.execute("SELECT * FROM users WHERE user_name = %s", (user_name,))
            result = cur.fetchone()

            column_names = [desc[0] for desc in cur.description]

            result_dict = dict(zip(column_names, result)) if result else None

            print(result_dict)
            return result_dict

        except Exception as e:
            print(f"Error: {e}")
            conn.rollback()
        finally:
            cur.close()
            conn.close()

    def get_all_users_list(self):
        cur, conn = connect()
        try:
            cur.execute("SELECT user_name, permissions, status FROM users ORDER BY user_id")
            result = cur.fetchall()
            print(result)
            return result
        except Exception as e:
            print(f"Error: {e}")
            conn.rollback()
        finally:
            cur.close()
            conn.close()

    def check_if_user_exist(self, user_name):
        cur, conn = connect()
        try:
            cur.execute("SELECT 1 FROM users WHERE user_name = %s", (user_name,))
            if cur.fetchone():
                return True  # User exist
            else:
                return False  # User not exist
        except Exception as e:
            print(f"Error: {e}")
            conn.rollback()
        finally:
            cur.close()
            conn.close()

    def inbox_msg_counting(self, recipient_id):
        cur, conn = connect()
        try:
            cur.execute("SELECT COUNT(*) FROM messages WHERE recipient_id = %s", (recipient_id,))
            count = cur.fetchone()[0]
            return count
        except Exception as e:
            print(f"Error: {e}")
            conn.rollback()
        finally:
            cur.close()
            conn.close()

    def check_if_user_is_logged_in(self, user_name):
        cur, conn = connect()
        try:
            cur.execute("SELECT login_time FROM users WHERE user_name = %s", (user_name,))
            result = cur.fetchone()
            if result and result[0] is not None:
                return True  # User is looged in
            else:
                return False  # User is not logged in
        except Exception as e:
            print(f"Error: {e}")
            conn.rollback()
        finally:
            cur.close()
            conn.close()

    def create_db_account(self, table, new_user_data):
        cur, conn = connect()
        try:
            query = sql.SQL("INSERT INTO {} (user_name, password, permissions, status, activation_date) VALUES (%s, %s, %s, %s, %s)").format(sql.Identifier(table))
            cur.execute(query.as_string(conn), new_user_data)
            conn.commit()
        except Exception as e:
            print(f"Error: {e}")
            conn.rollback()
        finally:
            cur.close()
            conn.close()
