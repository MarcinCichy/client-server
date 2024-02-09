import psycopg2
from psycopg2 import connect as pg_connect
from server_package.config import db_config
import server_package.server_response as server_response


def connect():
    try:
        print('Connecting to the PostgreSQL database...')
        params = db_config()
        return pg_connect(**params)
    except (Exception, psycopg2.DatabaseError) as e:
        print(f"Connection error = {e}")
        print('Database connection failed.')
        # return {"Error": str(e)}
        return {server_response.E_DATABASE_ERROR}
