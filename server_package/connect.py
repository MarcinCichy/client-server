import psycopg2
from config import config


def connect():
    conn = None
    try:
        params = config()
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        cur = conn.cursor()

        print('PostgreSQL database version:')
        cur.execute('SELECT version()')
        db_version = cur.fetchone()
        print(db_version)

        print('List of PosgresSQL databases:')
        cur.execute('SELECT datname FROM pg_database;')
        db_list = cur.fetchall()
        print(db_list)

        print("List of database's tables:")
        cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        for table in cur.fetchall():
            print(table)

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


if __name__ == '__main__':
    connect()
