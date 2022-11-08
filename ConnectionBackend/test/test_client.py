import socket
import sys
import socket
import time
import json
import threading

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

HOST, PORT = "127.0.0.1", 9999

USERNAME = 'flinnfx#101'

# noinspection PyTypeChecker


# SOCK_DGRAM is the socket type to use for UDP sockets
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def threaded_receiver():
    while True:
        print('Receiving...')
        print(str(sock.recv(1024), 'utf-8'))
        print('Received.')


sock.sendto(bytes('01{"Login": "flinnfx"}', "utf-8"), (HOST, PORT))
receiver_thread = threading.Thread(target=threaded_receiver).start()

# As you can see, there is no connect() call; UDP has no connections.
# Instead, data is directly sent to the recipient via sendto().

# received = str(sock.recv(1024), "utf-8")

while True:
    data: dict = {
        'Message': 'My Message',
        'SendTime': time.time(),
        'From': USERNAME,
        'To': 'flinnfx#101'
    }
    data: str = '02' + json.dumps(data)
    sock.sendto(bytes(data, "utf-8"), (HOST, PORT))

# print("Sent:     {}".format(data))
# print("Received: {}".format(received))
