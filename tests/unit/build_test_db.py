import psycopg2
import bcrypt
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from tests.unit.test_config import test_db_config

params = test_db_config()

temp_db_name = 'test_database'


def create_temp_db():
    conn = psycopg2.connect(dbname='db_CS', user=params['user'], password=params['password'], host=params['host'])
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute(f'CREATE DATABASE "{temp_db_name}";')

    conn_temp = psycopg2.connect(dbname=temp_db_name, user=params['user'], password=params['password'],
                                 host=params['host'])
    cur_temp = conn_temp.cursor()
    cur_temp.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id serial PRIMARY KEY,
            user_name varchar(50) NOT NULL UNIQUE,
            permissions varchar(5) NOT NULL,
            status varchar(6) NOT NULL,
            activation_date date NOT NULL,
            login_time timestamp without time zone
        );
        """)
    cur_temp.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            message_id serial PRIMARY KEY,
            sender_id varchar(50),
            date date NOT NULL,
            recipient_id varchar(50) REFERENCES users(user_name) ON DELETE CASCADE,
            content varchar(250)
        );
        """)
    cur_temp.execute("""
       CREATE TABLE IF NOT EXISTS passwords (
           user_id integer NOT NULL,
           hashed_password bytea NOT NULL,
           salt bytea NOT NULL,
           PRIMARY KEY (user_id),
           FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
       );
       """)
    conn_temp.commit()
    cur_temp.close()
    conn_temp.close()

    cur.close()
    conn.close()
    print(f'Testing database with tables was created')


def drop_temp_db():
    conn = psycopg2.connect(dbname='postgres', user=params['user'], password=params['password'], host=params['host'])
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    # All connection to db was finished
    cur.execute(f"""
    SELECT pg_terminate_backend(pg_stat_activity.pid)
    FROM pg_stat_activity
    WHERE pg_stat_activity.datname = '{temp_db_name}'
      AND pid <> pg_backend_pid();
    """)

    cur.execute(f"DROP DATABASE IF EXISTS {temp_db_name};")
    cur.close()
    conn.close()
    print(f'Testing database was dropped')


def fill_temp_db():
    print("Test tables filling was started")
    conn = psycopg2.connect(dbname=temp_db_name, user=params['user'], password=params['password'], host=params['host'])
    cur = conn.cursor()

    users_data = [
        ("user1", "admin", "active", "2024-02-18"),
        ("user2", "user", "banned", "2024-02-18"),
        ("user3", "user", "active", "2024-02-18"),
        ("user4", "admin", "active", "2024-02-18"),
        ("user5", "user", "banned", "2024-02-18")
    ]
    # Passwords corresponding to users, for simplicity, user_name + 'password'
    passwords = ["password1", "password2", "password3", "password4", "password5"]

    for idx, user_data in enumerate(users_data):
        cur.execute(
            "INSERT INTO users (user_name, permissions, status, activation_date) VALUES (%s, %s, %s, %s) RETURNING user_id",
            user_data
        )
        user_id = cur.fetchone()[0]  # Pobranie wygenerowanego user_id

        # Hashing the password with bcrypt
        password = passwords[idx].encode('utf-8')
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

        # Wstawianie zaszyfrowanego hasła i soli do tabeli passwords
        cur.execute(
            "INSERT INTO passwords (user_id, hashed_password, salt) VALUES (%s, %s, %s)",
            (user_id, hashed_password, hashed_password[:29])  # Przykład z solą; dostosuj według potrzeb
        )

    messages_data = [
        ("user1", "2024-02-18", "user1", "Hello, user2!"),
        ("user2", "2024-02-18", "user2", "Hi there, user3!"),
        ("user1", "2024-02-18", "user3", "Hey user4, how are you?"),
        ("user4", "2024-02-18", "user1", "Greetings, user5!"),
        ("user4", "2024-02-18", "user5", "Welcome, user1!"),
        ("user2", "2024-02-18", "user1", "Hello, user2!"),
        ("user3", "2024-02-18", "user1", "Hello, user2!"),
        ("user5", "2024-02-18", "user1", "Hello, user2!")
    ]
    for message_data in messages_data:
        cur.execute(
            "INSERT INTO messages (sender_id, date, recipient_id, content) VALUES (%s, %s, %s, %s)",
            message_data
        )

    conn.commit()
    cur.close()
    conn.close()
    print("Test tables filling was finished")
