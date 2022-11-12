import json
import pickle
import sqlite3
import secrets
from typing import Tuple, Any

import pandas as pd
import time
from secrets import compare_digest


# todo: Still have to create a __new_cursor for every function so there will be no multithreading
#  conflict in the future with a lot of requests to the API.

# pd.set_option('display.max_columns', None)

# TODO: Store the public key in database. Update it on activate and deactive and write a function
#  to return him. Also maybe to change him manually

# "active" means
# "authenticated" means the email is okay.


class Database:
    def __init__(self, db_path: str, pickle_path: str):
        self.used = False
        self.query = list()
        self.connection = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.db_path = db_path
        self.pickle_path = pickle_path

    def __del__(self):
        self.connection.commit()
        self.cursor.close()
        self.connection.close()

    def __str__(self):
        table = pd.read_sql_query('SELECT * FROM users', con=self.connection)

        return str(table.columns.values) + '\n' + str(table)

    def get_password(self, id: int):
        __new_cursor = self.connection.cursor()
        __new_cursor.execute("SELECT password FROM users WHERE id = ?", (id,))
        password = __new_cursor.fetchone()[0]
        __new_cursor.close()
        return password

    def add_user(self, username: str, email: str, password: str) -> tuple[int | Any, str]:
        """
        :param username:
        :param email:
        :param password: str: The hashed Password. Algorithm blake2b is used in the script.
        :return:
        """
        # get the highest id from the Database
        __new_cursor = self.connection.cursor()
        __new_cursor.execute("SELECT MAX(id) FROM users")
        self.connection.commit()
        id = __new_cursor.fetchone()[0]
        if id is None:
            id = 1
        else:
            id += 1

        auth_token = secrets.token_urlsafe(8)

        __new_cursor.execute(
            "INSERT INTO users ( username, userid, email, password, auth_token) VALUES ("
            "?, "
            "?, ?, "
            "?, ?)", (username, f'{username}#{id}', email, password, auth_token))

        __new_cursor.execute(f'''
        CREATE TABLE "{id}"(
            friend_id INTEGER PRIMARY KEY NOT NULL 
        )
        ''')

        self.connection.commit()
        return id, auth_token

    def generate_api_key(self, id: int):
        # generate api token
        api_key = secrets.token_urlsafe(64)
        # get linux timestamp
        timestamp = int(time.time())
        # store token and time in a list to serialize it to json to store it in the Database
        api_list = [timestamp, api_key]
        # add the serialized list to the Database
        self.cursor.execute("UPDATE users SET api_key = ? WHERE id = ?", (json.dumps(api_list), id))
        self.connection.commit()
        return api_key

    def get_api_key(self, id: int):
        __new_cursor = self.connection.cursor()
        __new_cursor.execute("SELECT api_key FROM users WHERE id = ?", (id,))
        api_key = __new_cursor.fetchone()
        return api_key

    def update_api_key(self, id: int):
        api_key_db = self.get_api_key(id)
        try:
            api_key_db = json.loads(api_key_db[0])
        except TypeError:
            try:
                api_key_db = json.loads(api_key_db)
            except TypeError as error:
                return False, error

        if int(time.time()) - api_key_db[0] > 172800:
            # clear api_key if it is older than 2 days
            self.cursor.execute("UPDATE users SET api_key = ? WHERE id = ?", (None, id))
            self.connection.commit()
            return False
        return True

    def check_api_key(self, id: int, api_key: str):
        api_key_db = self.get_api_key(id)
        try:
            api_key_db = json.loads(api_key_db[0])
        except TypeError:
            return False
        if api_key_db[1] == api_key:
            return True
        else:
            return False

    def get_all_users(self) -> list:
        self.cursor.execute("SELECT * FROM users")
        data = self.cursor.fetchall()
        newdata = list()
        for entry in data:
            entry = list(entry)
            entry[5] = json.loads(entry[5])
            newdata.append(entry)
        return newdata

    def get_contacts(self, id: int) -> list:
        self.cursor.execute("SELECT contacts FROM users WHERE id = ?", (id,))
        contacts = self.cursor.fetchone()[0]
        if contacts is None:
            return []
        else:
            return json.loads(contacts)

    def add_friend(self, id: int, friend_id: int):
        if not self.check_user(friend_id):
            return False, 'friend id not valid'
        if not self.check_user(id):
            return False, 'id not valid'

        __new_cursor = self.connection.cursor()
        try:
            __new_cursor.execute(f'''
                INSERT INTO "{id}" (friend_id) VALUES ({friend_id})
            ''')

            __new_cursor.execute(f'''
                INSERT INTO "{friend_id}" (friend_id) VALUES ({id})
            ''')
        except sqlite3.IntegrityError:
            return False, 'Already Friends'
        self.connection.commit()
        __new_cursor.close()
        return True

    def remove_friend(self, id: int, friend_id: int):
        __new_cursor = self.connection.cursor()
        __new_cursor.execute(f'''
        DELETE FROM "{id}" WHERE friend_id="{friend_id}"
        ''')

        __new_cursor.execute(f'''
        DELETE FROM "{friend_id}" WHERE friend_id="{id}"
        ''')

        self.connection.commit()
        __new_cursor.close()

    def get_friends(self, id: int):
        __new_cursor = self.connection.cursor()
        __new_cursor.execute(f'''
        SELECT * FROM "{id}"
        ''')

        result = __new_cursor.fetchall()

        __new_cursor.close()
        return [int(f_id[0]) for f_id in result]

    def _add_contact(self, id: int, contact_id: int) -> None:
        """
        DEPRECATED DO NOT USE!

        :param id:
        :param contact_id:
        :return:
        """

        # Deprecated don't use!
        # For the ID user
        self.cursor.execute("SELECT contacts FROM users WHERE id = ?", (id,))
        contacts = self.cursor.fetchone()[0]
        if contacts is None:
            contacts = []
        else:
            contacts = json.loads(contacts)
        contacts.append(contact_id)
        contacts = list(set(contacts))
        self.cursor.execute("UPDATE users SET contacts = ? WHERE id = ?",
                            (json.dumps(contacts), id))
        # For the contact user
        self.cursor.execute("SELECT contacts FROM users WHERE id = ?", (contact_id,))
        contacts = self.cursor.fetchone()[0]
        if contacts is None:
            contacts = []
        else:
            contacts = json.loads(contacts)
        contacts.append(id)
        contacts = list(set(contacts))
        self.cursor.execute("UPDATE users SET contacts = ? WHERE id = ?",
                            (json.dumps(contacts), contact_id))
        # Commit for both users
        self.connection.commit()

    def _remove_contact(self, id: int, contact_id: int) -> None:
        """
        DEPRECATED DO NOT USE!
        :param id:
        :param contact_id:
        :return:
        """
        self.cursor.execute("SELECT contacts FROM users WHERE id = ?", (id,))
        contacts = self.cursor.fetchone()[0]
        if contacts is None:
            contacts = []
        else:
            contacts = json.loads(contacts)
        contacts.remove(contact_id)
        self.cursor.execute("UPDATE users SET contacts = ? WHERE id = ?",
                            (json.dumps(contacts), id))
        self.connection.commit()

    def check_contact(self, id: int, contact_id: int) -> bool:
        __new_cursor = self.connection.cursor()
        __new_cursor.execute("SELECT contacts FROM users WHERE id = ?", (id,))
        contacts = __new_cursor.fetchone()[0]
        if contacts is None:
            __new_cursor.close()
            return False
        else:
            contacts = json.loads(contacts)
            if contact_id in contacts:
                __new_cursor.close()
                return True
            else:
                __new_cursor.close()
                return False

    def check_user(self, id: int) -> bool:
        __new_cursor = self.connection.cursor()
        __new_cursor.execute("SELECT * FROM users WHERE id = ?", (id,))
        if __new_cursor.fetchone() is None:
            __new_cursor.close()
            return False
        else:
            __new_cursor.close()
            return True

    def get_messages(self, id: int, other_id: int = None):
        __new_cursor = self.connection.cursor()
        if other_id is None:
            __new_cursor.execute("SELECT * FROM messages WHERE ids LIKE ?", (f'%{id}%',))
            ids = __new_cursor.fetchall()
            newdata = list()
            for entry in ids:
                entry = list(entry)
                entry[0] = json.loads(entry[0])
                newdata.append(entry)
            __new_cursor.close()
            return newdata
        else:
            __new_cursor.execute("SELECT * FROM messages WHERE ids LIKE ?", (f'%{id}%',))
            ids = __new_cursor.fetchall()
            newdata = list()
            for entry in ids:
                entry = list(entry)
                entry[0] = json.loads(entry[0])
                if other_id in entry[0]:
                    newdata.append(entry)
            __new_cursor.close()
            return newdata

    def add_message(self, ids: list[int], message: str):
        __new_cursor = self.connection.cursor()
        # get linux timestamp
        timestamp = int(time.time())

        ids_json = json.dumps(ids)

        # make message not harmful to the database
        message = message.replace("'", "''")

        __new_cursor.execute("INSERT INTO messages ( ids, message, timestamp) VALUES (?, ?, ?)",
                             (ids_json, message, timestamp))
        self.connection.commit()
        __new_cursor.close()

    def change_password(self, id: int, new_password_hash: str):
        __new_cursor = self.connection.cursor()
        __new_cursor.execute("UPDATE users SET password = ? WHERE id = ?", (new_password_hash, id))
        self.connection.commit()
        __new_cursor.close()

    def _change_password(self, id: int, password: str, new_password_hash: str):
        __new_cursor = self.connection.cursor()
        __new_cursor.execute("SELECT password FROM users WHERE id = ?", (id,))
        old_password = __new_cursor.fetchone()[0]
        if compare_digest(old_password, password):
            self._change_password(id, new_password_hash)
            __new_cursor.close()
            return True
        __new_cursor.close()
        return new_password_hash

    def authenticate(self, id: int):
        __new_cursor = self.connection.cursor()
        __new_cursor.execute('UPDATE users SET authenticated = ? WHERE id = ?', (True, id))
        self.connection.commit()
        __new_cursor.close()

    def deauthenticate(self, id: int):
        __new_cursor = self.connection.cursor()
        __new_cursor.execute('UPDATE users SET authenticated = ? WHERE id = ?', (False, id))
        self.connection.commit()
        __new_cursor.close()

    def is_authenticated(self, id):
        __new_cursor = self.connection.cursor()
        __new_cursor.execute('SELECT authenticated FROM users WHERE id = ?', (id,))
        if __new_cursor.fetchone()[0]:
            __new_cursor.close()
            return True
        __new_cursor.close()
        return False

    def activate(self, id: int, ip: tuple):
        ip = json.dumps(ip)
        __new_cursor = self.connection.cursor()
        __new_cursor.execute('UPDATE users SET active = ? WHERE id = ?', (True, id))
        __new_cursor.execute('UPDATE users SET ip_address = ? WHERE id = ?', (ip, id))
        self.connection.commit()
        __new_cursor.close()

    def deactivate(self, id: int):
        __new_cursor = self.connection.cursor()
        __new_cursor.execute('UPDATE users SET active = ? WHERE id = ?', (False, id))
        __new_cursor.execute('UPDATE users SET ip_address = ? WHERE id = ?', ('NOT_DEFINED', id))
        self.connection.commit()
        __new_cursor.close()

    def get_active_users_unfinished(self) -> list:
        __new_cursor = self.connection.cursor()
        __new_cursor.execute("SELECT * FROM users WHERE active = ?", (True,))
        data = __new_cursor.fetchall()
        newdata = list()
        for entry in data:
            entry = list(entry)
            entry[5] = json.loads(entry[5])
            newdata.append(entry)
        __new_cursor.close()
        return newdata

    def is_active(self, user_id: int):
        __new_cursor = self.connection.cursor()
        __new_cursor.execute("SELECT active FROM users WHERE id = ?", (user_id,))
        active = __new_cursor.fetchone()[0]
        if active:
            return True
        __new_cursor.close()
        return False

    def _get_user_by_id(self, id: int):
        __new_cursor = self.connection.cursor()
        __new_cursor.execute("SELECT * FROM users WHERE id = ?", (id,))
        data = __new_cursor.fetchone()
        __new_cursor.close()
        return data

    def get_user_name_by_id(self, id: int):
        if self.check_user(id):
            userstring = self._get_user_by_id(id)
            return userstring[1]
        return None

    def get_ip_of_user(self, id: int):
        if self.check_user(id):
            __new_cursor = self.connection.cursor()
            __new_cursor.execute(f'SELECT ip_address FROM users WHERE id = {id}')
            ip = __new_cursor.fetchone()
            ip = json.loads(ip[0])
            __new_cursor.close()
            return tuple(ip)

    def _update_ip_of_user(self, id: int, ip: tuple):
        if self.check_user(id):
            __new_cursor = self.connection.cursor()
            __new_cursor.execute(f'UPDATE users SET ip_address = ? WHERE id = ?', (ip, id))
            self.connection.commit()
            __new_cursor.close()

    def get_public_key_of_user(self, id: int):
        __new_cursor = self.connection.cursor()
        __new_cursor.execute(f'SELECT public_key FROM users WHERE id = {id}')

        key = __new_cursor.fetchone()

        __new_cursor.close()
        return key

    def is_online(self, id: int):
        if not self.check_user(id):
            return None
        else:
            __new_cursor = self.connection.cursor()
            __new_cursor.execute(f'''
            SELECT online from users WHERE id = ?
            ''', (True,))

            online = __new_cursor.fetchone()

            return False if online[0] == 0 else True

    def set_online(self, id: int, ip: tuple) -> object:
        ip = json.dumps(ip)
        __new_cursor = self.connection.cursor()
        __new_cursor.execute('UPDATE users SET ip_address = ? WHERE id = ?', (ip, id))
        __new_cursor.execute('UPDATE users SET online = ? WHERE id = ?', (True, id))

        self.connection.commit()
        __new_cursor.close()
        return True

    def set_offline(self, id: int):
        __new_cursor = self.connection.cursor()
        __new_cursor.execute('UPDATE users SET online = ? WHERE id = ?', (False, id))
        __new_cursor.execute('UPDATE users SET ip_address = ? WHERE id = ?', ('NOT_DEFINED', id))

        self.connection.commit()
        __new_cursor.close()
        return True


    def update_crypt_keys(self, public_key, private_key):
        with open(self.pickle_path, 'wb') as pickle_file:
            pickle.dump((public_key, private_key), pickle_file)

    def get_crypt_keys(self):
        with open(self.pickle_path, 'rb') as pickle_file:
            keys: tuple = pickle.load(pickle_file)
            return keys

    def close(self):
        self.__del__()
