import hashlib

import models

connection = models.ServerConnection(('127.0.0.1', 9999),
                                     userid='flinnfx#1',
                                     hashed_password=hashlib.blake2b('abc'.encode(
                                         'utf-8')).hexdigest())

print(connection.api_key)
print(connection.server_public_key)
connection.send_message('Hello how are you today?', receiver='tcgamer#102', debug=True)

connection.sock.recv(2048)
