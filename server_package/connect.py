import psycopg2
from config import config


def connect():
    """Nawiązuje połączenie z bazą danych i zwraca kursor."""
    conn = None
    try:
        params = config()
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        return conn.cursor(), conn  # Zwróć kursor i połączenie
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        if conn is not None:
            conn.close()
        print('Database connection closed.')
