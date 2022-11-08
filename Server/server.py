# pyright: reportGeneralTypeIssues=false, reportMissingImports=false
import socketserver
import models
import datetime
import sys

#sys.path.append(r'C:\Users\Flinn\Documents\Chat')
sys.path.append('..')

import database.tools

database = database.tools.Database('server.db')

print(database)

database.activate(101, ('127.0.0.1', 52303))



class UDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        message = models.BaseMessage(data)
        print(message.message_type)
        print(self.client_address)
        if message.message_type == models.MessageType.RegisterMessage:
            message: models.RegisterMessage
            socket.sendto('RegisterMessage is not supported yet!'.encode('utf-8'),
                          self.client_address)
        elif message.message_type == models.MessageType.ClassicMessage:
            message: models.ClassicMessage
            id: int = int(message.to.split('#')[1])
            if database.check_user(id) is not True:
                # send back that the user does not exist or his account is not activated and return
                ...
            ip = database.get_ip_of_user(id)
            print('Ip')
            print(ip)
            socket.sendto('Message Received'.encode('utf-8'), self.client_address)
        elif message.message_type == models.MessageType.LoginMessage:
            message: models.LoginMessage
            message.ip = self.client_address # type: ignore 
            

        print(f'''
            Message from: {self.client_address[0]}
              To: {message.to}
            Sent: {datetime.datetime.utcfromtimestamp(message.send_time).strftime('%d-%m-%Y | %H:%M:%S')}
            Message: {message.text}
        ''')

        print('----------')
        print(f'{self.client_address[0]} wrote: {data}')
        socket.sendto(data.upper(), self.client_address)


if __name__ == '__main__':
    HOST, PORT = '127.0.0.1', 9999

    with socketserver.UDPServer((HOST, PORT), UDPHandler) as server:
        server.serve_forever()
