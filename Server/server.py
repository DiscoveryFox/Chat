# pyright: reportGeneralTypeIssues=false, reportMissingImports=false
import json
import socket
import socketserver

import rsa

import models
import datetime
import sys

# sys.path.append(r'C:\Users\Flinn\Documents\Chat')
sys.path.append('..')

import database.tools
import database.custom_crypt as crypt

database = database.tools.Database('server.db', 'server.pickle')

# print(database)

database.activate(101, ('127.0.0.1', 52303))

public_key, private_key = database.get_crypt_keys()


def test_keys():
    test_value_one = 'All inner cows view each other, only fraternal saints have a history.'
    enc_test_value_one = rsa.encrypt(test_value_one.encode('utf-8'), public_key)
    dec_test_value_one = rsa.decrypt(enc_test_value_one, private_key).decode('utf-8')
    assert test_value_one == dec_test_value_one
    return test_value_one == dec_test_value_one


print('-----------')
print(private_key)
print(public_key)

print('Checking Keys...')
print(test_keys())
print('Check done!')
print('-----------')
print()

if public_key is None or private_key is None:
    print('Generating new Keys')
    crypt.gen_new_keys(database)


class UDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip()
        sock: socket.SocketType = self.request[1]
        message = models.BaseMessage(data, private_key)
        if message.message_type == models.MessageType.RegisterMessage:
            message: models.RegisterMessage
            sock.sendto('RegisterMessage is not supported yet!'.encode('utf-8'),
                        self.client_address)
        elif message.message_type == models.MessageType.ClassicMessage:
            message: models.ClassicMessage
            id: int = int(message.to.split('#')[1])
            print(message.text)
            if database.check_user(id) is not True:
                # send back that the user does not exist or his account is not activated and return
                return
            if database.is_active(id) is not True:
                return
            ip = database.get_ip_of_user(id)
            sock.sendto('Message Received'.encode('utf-8'), self.client_address)
        elif message.message_type == models.MessageType.LoginMessage:
            message: models.LoginMessage
            message.ip = self.client_address  # type: ignore

            if database.is_active(message.id):
                sock.sendto(crypt.encrypt(data='01User is already logged in.',
                                          public_key=message.client_public_key),
                            message.ip)
                return
            database.activate(message.id, message.ip)
            api_key = database.generate_api_key(message.id)
            print(message.client_public_key)
            sock.sendto(crypt.encrypt(data=api_key, public_key=message.client_public_key),
                        message.ip)
        elif message.message_type == models.MessageType.LogoutMessage:
            message: models.LogoutMessage
            message.ip = self.client_address

            database.deactivate(message.id)

            '''
            1. Need to create the message structure
                mesage {
                        message_type
                        ip
                        userid
                        hashed_password
                        }
            2. check if user is currently logged in. Maybe log him out then
            3. check if the password is correct.
            4. log the user in -> activate, generate API-key, set ip
            5. return the api-key to the requester
            '''
        elif message.message_type == models.MessageType.ServePublicKey:
            message: models.ServePublicKey

            message.ip = self.client_address
            sock.sendto(crypt.key_to_str(public_key), message.ip)

        # print(f'{self.client_address[0]} wrote: {data}')
        # sock.sendto(data.upper(), self.client_address)


if __name__ == '__main__':
    HOST, PORT = '127.0.0.1', 9999

    with socketserver.UDPServer((HOST, PORT), UDPHandler) as server:
        server.serve_forever()
