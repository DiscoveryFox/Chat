# DEPRECATED DO NOT USE!

import sqlite3

import sqlalchemy as db
import sqlalchemy.orm
import pandas as pd
import models

dbEngine = db.create_engine('sqlite:///C:\\Users\\Flinn\\Documents\\Chat\\Server\\server.db')
Session = sqlalchemy.orm.sessionmaker(bind=dbEngine)
session = Session()
metadata = db.MetaData()
inspector: db.engine.reflection.Inspector = db.inspect(dbEngine)


def get_user_table():
    return db.Table('users', metadata, autoload=True, autoload_with=dbEngine)


def create_user_table(meta=metadata, engine=dbEngine):
    db.Table(
        'users', meta,
        db.Column('username', db.TEXT, primary_key=True),
        db.Column('ip_address', db.TEXT),
        db.Column('online', db.BOOLEAN),
        db.Column('email_address', db.TEXT, unique=True)
    )

    meta.create_all(engine)


def register_user(username: str, ip_address: str, online: bool = False,
                  email_address: str = None, engine=dbEngine):
    if check_if_user_exists(username):
        return models.UserAlreadyExists(username)
    stmt = db.insert(get_user_table()).values(username=username, ip_address=ip_address,
                                              online=online, email_address=email_address)
    with engine.connect() as conn:
        return conn.execute(stmt)


def show_table(table_name: str = 'users', engine: db.engine.Engine = dbEngine):
    print(pd.read_sql_table(table_name=table_name, con=engine))


def check_if_user_exists(username: str, engine=dbEngine):
    with engine.connect() as conn:
        return True if username in [x[0] for x in
                                    conn.execute('SELECT * FROM users').fetchall()] else False


def get_ip_of_user(username: str, engine=dbEngine):
    with engine.connect() as conn:
        result = conn.execute(f'SELECT ip_address FROM users WHERE username='
                              f'"{username}"').fetchall()
        return result


# noinspection SqlResolve
def drop_table(engine=dbEngine):
    engine.execute('DROP TABLE users')


x = register_user('flinnfx', 'localhost', False, 'root@root.de')
print(x)
print()
print(check_if_user_exists('flin365'))
show_table()

print(get_ip_of_user('flinnfx'))
