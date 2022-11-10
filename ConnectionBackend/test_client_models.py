import hashlib

import models

connection = models.ServerConnection(('127.0.0.1', 9999),
                                     userid='flinnfx#101',
                                     hashed_password=hashlib.blake2b('abc'.encode(
                                         'utf-8')).hexdigest())

connection.send_message('Hello how are you today?', receiver='marc#100')
