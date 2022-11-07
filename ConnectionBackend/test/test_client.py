import socket
import sys
import socket
import time
import json

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

HOST, PORT = "127.0.0.1", 9999

USERNAME = 'flinnfx'

data: dict = {
    'Message': input('Message: '),
    'SendTime': time.time(),
    'From': USERNAME,
    'To': input('To: ')
}

# noinspection PyTypeChecker
data = '02' + json.dumps(data)

# SOCK_DGRAM is the socket type to use for UDP sockets
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# As you can see, there is no connect() call; UDP has no connections.
# Instead, data is directly sent to the recipient via sendto().
sock.sendto(bytes(data, "utf-8"), (HOST, PORT))
received = str(sock.recv(1024), "utf-8")

print("Sent:     {}".format(data))
print("Received: {}".format(received))
