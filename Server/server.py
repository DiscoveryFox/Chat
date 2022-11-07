import socketserver
import models
import datetime
import sys

sys.path.append(r'C:\Users\Flinn\Documents\Chat')

import database.tools

database = database.tools.Database('server.db')

print(database)


class UDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip()
        print('----------')
        socket = self.request[1]
        message = models.BaseMessage(data)
        print(message.MessageType)
        print(f'''
            Message from: {self.client_address[0]}
            To: {message.To}
            Sent: {datetime.datetime.utcfromtimestamp(message.SendTime).strftime('%d-%m-%Y | %H:%M:%S')}
            Message: {message.Text}
        ''')

        print('----------')
        print(f'{self.client_address[0]} wrote: {data}')
        socket.sendto(data.upper(), self.client_address)


if __name__ == '__main__':
    HOST, PORT = '127.0.0.1', 9999

    with socketserver.UDPServer((HOST, PORT), UDPHandler) as server:
        server.serve_forever()
