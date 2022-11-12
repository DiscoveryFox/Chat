import socket
import sys
import socket
import time
import json
import threading
import rsa
import hashlib

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

HOST, PORT = "127.0.0.1", 9999

USERNAME = 'flinnfx#101'


# noinspection PyTypeChecker,DuplicatedCode


def encrypt(data: str, public_key, encoding: str = 'utf-8') -> bytes:
    result: list = []
    for n in range(0, len(data), 245):
        part = data[n:n + 245]
        result.append(rsa.encrypt(part.encode(encoding), public_key))
    return b''.join(result)


def decrypt(data: bytes, private_key, encoding: str = 'utf-8') -> str:
    result: list = []
    for n in range(0, len(data), 256):
        part = data[n:n + 256]
        decrypted_part = rsa.decrypt(part, private_key).decode(encoding)
        result.append(decrypted_part)
    return ''.join(result)


def send_message(message_text: str,
                 api_key: str,
                 server_public_key,
                 server: tuple = (HOST, PORT),
                 encoding: str = 'utf-8'):
    encrypt('02' + json.dumps({
        'Message': message_text,
        'SendTime': time.time(),
        'ApiKey': api_key,
        'To': 'flinnfx#101'
    }), server_public_key)


# SOCK_DGRAM is the socket type to use for UDP sockets
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def threaded_receiver():
    while True:
        print('Receiving...')
        print(str(sock.recv(1024), 'utf-8'))

        print('Received.')


sock.sendto(bytes('04{}', 'utf-8'), (HOST, PORT))
# receiver_thread = threading.Thread(target=threaded_receiver).start()

# As you can see, there is no connect() call; UDP has no connections.
# Instead, data is directly sent to the recipient via sendto().

# received = str(sock.recv(1024), "utf-8")

while False:
    data: dict = {
        'Message': 'My Message',
        'SendTime': time.time(),
        'From': USERNAME,
        'To': 'flinnfx#101'
    }
    data: str = '02' + json.dumps(data)
    sock.sendto(bytes(data, "utf-8"), (HOST, PORT))

# sock.sendto(bytes('04{}', 'utf-8'), (HOST, PORT))
key_str = sock.recv(1024)
server_publicKey = rsa.key.PublicKey.load_pkcs1(key_str)

client_public_key, client_private_key = rsa.newkeys(2048)

print(client_public_key)

PASSWORD = hashlib.blake2b(bytes('abc', 'utf-8')).hexdigest()

login_data: dict = {
    'UserID': USERNAME,
    'Password': PASSWORD,
    'client_public_key': client_public_key.save_pkcs1().decode('utf-8')
}

data: dict = {
    'Message': 'This is an Example message. It should be encrypted',
    'SendTime': time.time(),
    'From': USERNAME,
    'To': 'flinnfx#101'
}
data: str = json.dumps(data)
data: str = '02' + data
login_data: str = '01' + json.dumps(login_data)
data: bytes = rsa.encrypt(data.encode('utf-8'), server_publicKey)
print(len(login_data))
result: list = []

for n in range(0, len(login_data), 245):
    part = login_data[n:n + 245]
    result.append(rsa.encrypt(part.encode('utf-8'), server_publicKey))

# login_data: bytes = rsa.encrypt(login_data.encode('utf-8'), server_publicKey)
login_data: bytes = b''.join(result)
print(login_data)
print('Sending data...')
sock.sendto(login_data, (HOST, PORT))
api_key = decrypt(sock.recv(1024), client_private_key)
while True:
    y = sock.recv(1024)
    try:
        x = decrypt(y, client_private_key)
        print('Answer:')
        print(x)
        print('Answer End')
    except rsa.pkcs1.DecryptionError:
        print('Content is not encrypted!')
        print(y)
print('end')


# print(server_publicKey)
# print(type(server_publicKey))

# print("Sent:     {}".format(data))
# print("Received: {}".format(received))
send_message('Hello World!', api_key, server_publicKey)
