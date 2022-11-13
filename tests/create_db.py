import sqlite3

connection = sqlite3.connect(r'C:\Users\Flinn\Documents\Chat\Server\server.db')

cursor = connection.cursor()

# create a table with two fields

cursor.execute("""CREATE TABLE users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) NOT NULL,
    userid VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL UNIQUE,
    password TEXT NOT NULL,
    api_key TEXT UNIQUE,
    contacts TEXT,
    authenticated BOOLEAN NOT NULL DEFAULT FALSE,
    auth_token TEXT UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    active BOOLEAN NOT NULL DEFAULT TRUE,
    online BOOLEAN NOT NULL DEFAULT FALSE,
    ip_address TEXT NOT NULL DEFAULT 'NOT_DEFINED',
    public_key TEXT 
)""")

cursor.execute("""CREATE TABLE messages (
    ids TEXT NOT NULL,
    message TEXT NOT NULL,
    timestamp INTEGER NOT NULL,
    message_id INTEGER PRIMARY KEY AUTOINCREMENT
)""")

connection.commit()

connection.close()


# test : a71079d42853dea26e453004338670a53814b78137ffbed07603a41d76a483aa9bc33b582f77d30a65e6f29a896c0411f38312e1d66e0bf16386c86a89bea572

# password.txt: 7c863950ac93c93692995e4732ce1e1466ad74a775352ffbaaf2a4a4ce9b549d0b414a1f3150452be6c7c72c694a7cb46f76452917298d33e67611f0a42addb8