import os
from configparser import ConfigParser


def test_db_config(filename='test_database.ini', section='test_postgresql'):
    print(f"Trying to read config from: {os.path.abspath(filename)}")
    parser = ConfigParser()
    parser.read(filename)

    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} not found in the {filename} file')
    print(f"File {os.path.abspath(filename)} was read successfully")
    return db
