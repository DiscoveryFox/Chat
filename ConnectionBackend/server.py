import sys
import select
import socketserver


class UDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip()
        print('----------')
        print(data)
        socket = self.request[1]
        print(socket)
        print('----------')
        print(f'{self.client_address[0]} wrote: {data}')
        socket.sendto(data.upper(), self.client_address)
        socket.sendto('This is the second Message'.encode('utf-8'), self.client_address)


if __name__ == '__main__':
    HOST, PORT = '127.0.0.1', 9999

    with socketserver.UDPServer((HOST, PORT), UDPHandler) as server:
        server.serve_forever()

