import psycopg2
from server_package.config import db_config


def connect():
    conn = None
    try:
        params = db_config()
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        return conn.cursor(), conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        if conn is not None:
            conn.close()
            print('Database connection closed.')
