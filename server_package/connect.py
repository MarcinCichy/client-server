import psycopg2
from psycopg2 import connect as pg_connect
from server_package.config import db_config


def connect():
    try:
        print('Connecting to the PostgreSQL database...')
        params = db_config()
        return pg_connect(**params)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        print('Database connection failed.')
        return None
