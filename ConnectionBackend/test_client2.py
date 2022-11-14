import hashlib
import json
import models
import time

with models.ServerConnection(
    ('127.0.0.1', 9999),
    userid='tcgamer#102',
    hashed_password='8968535651071498e057c4fe2f71abfc76db12b655c3f7d517be7ff71e5b8273ac6d99df95e6936624f7abca7917fa2724085b7b907f1e7cd1e34594de3c0b4b'
) as connection:
    # 8968535651071498e057c4fe2f71abfc76db12b655c3f7d517be7ff71e5b8273ac6d99df95e6936624f7abca7917fa2724085b7b907f1e7cd1e34594de3c0b4b

    print(connection.api_key)
    print('Starting listening...')

    x = connection.sock.recv(2048)
    message: str = connection.decrypt(x)
    print(json.loads(message))

