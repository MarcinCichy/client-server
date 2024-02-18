import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from tests.unit.test_config import test_db_config

params = test_db_config()

temp_db_name = 'test_database'


def create_temp_db():
    conn = psycopg2.connect(dbname='db_CS', user=params['user'], password=params['password'], host=params['host'])
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute(f'CREATE DATABASE "{temp_db_name}";')

    conn_temp = psycopg2.connect(dbname=temp_db_name, user=params['user'], password=params['password'], host=params['host'])
    cur_temp = conn_temp.cursor()
    cur_temp.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id serial PRIMARY KEY,
        user_name varchar(50) NOT NULL,
        password varchar(50) NOT NULL,
        permissions varchar(5) NOT NULL,
        status varchar(6) NOT NULL,
        activation_date date NOT NULL,
        login_time timestamp without time zone,
        UNIQUE(user_name)
    );
    """)
    cur_temp.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        message_id serial PRIMARY KEY,
        sender_id varchar(50),
        date date NOT NULL,
        recipient_id varchar(50) REFERENCES users(user_name),
        content varchar(250)
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
        ("user1", "password1", "admin", "active", "2024-02-18"),
        ("user2", "password2", "user", "banned", "2024-02-18"),
        ("user3", "password3", "user", "active", "2024-02-18"),
        ("user4", "password4", "admin", "active", "2024-02-18"),
        ("user5", "password5", "user", "banned", "2024-02-18")
    ]
    for user_data in users_data:
        cur.execute(
            "INSERT INTO users (user_name, password, permissions, status, activation_date) VALUES (%s, %s, %s, %s, %s)",
            user_data
        )

    messages_data = [
        ("user1", "2024-02-18", "user1", "Hello, user2!"),
        ("user2", "2024-02-18", "user2", "Hi there, user3!"),
        ("user1", "2024-02-18", "user3", "Hey user4, how are you?"),
        ("user4", "2024-02-18", "user4", "Greetings, user5!"),
        ("user4", "2024-02-18", "user5", "Welcome, user1!")
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

# if __name__ == "__main__":
#     drop_temp_db()  # Usuwanie bazy po testach
#     create_temp_db()  # Tworzenie bazy i tabel w niej
#     fill_temp_db()  # Wypełnianie danymi
#
#     input(f'Nacisnij cos....')
#     drop_temp_db()  # Usuwanie bazy po testach
