import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from server_package.connect import connect
from psycopg2 import connect as pg_connect
from server_package.config import db_config

# Parametry połączenia do oryginalnej bazy danych
db_params = {
    'dbname': 'db_CS',
    'user': 'pozamiataj',
    'password': 'pozamiataj.pl',
    'host': '127.0.0.1'
}

# Nazwa tymczasowej bazy danych
temp_db_name = 'test_database'


# Tworzenie tymczasowej bazy danych
def create_temp_db():
    # Połączenie do domyślnej bazy danych, zwykle 'postgres', aby utworzyć nową bazę
    conn = psycopg2.connect(dbname='postgres', user=db_params['user'], password=db_params['password'],
                            host=db_params['host'])
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute(f'CREATE DATABASE "{temp_db_name}";')
    cur.close()
    conn.close()


# Usuwanie tymczasowej bazy danych
def drop_temp_db():
    conn = psycopg2.connect(**db_params)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute(f"DROP DATABASE IF EXISTS {temp_db_name};")
    cur.close()
    conn.close()


# Wypełnianie tymczasowej bazy danych fragmentem danych z oryginalnej bazy
def fill_temp_db():
    ## Połączenie z nowo utworzoną bazą danych
    conn = psycopg2.connect(dbname=temp_db_name, user=db_params['user'], password=db_params['password'], host=db_params['host'])
    cur = conn.cursor()

    # Utworzenie schematu tabel - przykład dla 'users' i 'messages', dostosuj zgodnie z potrzebami
    cur.execute("""
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
    cur.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        message_id serial PRIMARY KEY,
        sender_id varchar(50) REFERENCES users(user_name),
        date date NOT NULL,
        recipient_id varchar(50) REFERENCES users(user_name),
        content varchar(250)
    );
    """)

    # Połączenie z oryginalną bazą danych do skopiowania danych
    conn_orig = psycopg2.connect(**db_params)
    cur_orig = conn_orig.cursor()

    # Przechowywanie user_name skopiowanych użytkowników
    user_names = []

    # Kopiowanie 5 pierwszych rekordów z 'users'
    cur_orig.execute("SELECT * FROM users LIMIT 5;")
    users_rows = cur_orig.fetchall()
    for row in users_rows:
        cur.execute(
            "INSERT INTO users (user_name, password, permissions, status, activation_date, login_time) VALUES (%s, %s, %s, %s, %s, %s) RETURNING user_name",
            (row[1], row[2], row[3], row[4], row[5], row[6]))
        user_name = cur.fetchone()[0]  # Pobranie user_name z wstawionego rekordu
        user_names.append(user_name)

    # Kopiowanie 5 pierwszych rekordów z 'messages'
    for user_name in user_names:
        cur_orig.execute("SELECT * FROM messages WHERE sender_id = %s OR recipient_id = %s LIMIT 5;",
                         (user_name, user_name))
        messages_rows = cur_orig.fetchall()
        for row in messages_rows:
            cur.execute("INSERT INTO messages (sender_id, date, recipient_id, content) VALUES (%s, %s, %s, %s)",
                        (row[1], row[2], row[3], row[4]))

    # Zatwierdzenie zmian i zamknięcie połączeń
    conn.commit()
    cur.close()
    conn.close()
    cur_orig.close()
    conn_orig.close()


# Przykład użycia
if __name__ == "__main__":
    drop_temp_db()  # Usuwanie bazy po testach
    create_temp_db()  # Tworzenie bazy
    fill_temp_db()  # Wypełnianie danymi
    # Tutaj można wykonać testy...
    drop_temp_db()  # Usuwanie bazy po testach