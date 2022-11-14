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
    'All inner cows view each other, only fraternal saints have a history.'  # Dummy Text
    'All inner cows view each other, only fraternal saints have a history.'  # Dummy Text
    'All inner cows view each other, only fraternal saints have a history.'  # Dummy Text
    'All inner cows view each other, only fraternal saints have a history.'  # Dummy Text
    # dummy text
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

# TODO: Set get_user_of_api_key()[0] to get_user_of_api_key() without the [0]
# TODO: Check if the new is_online/offline works not instead of activate and/or deactive
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
            receiver_id: int = int(message.to.split('#')[1])
            message.id = database.get_user_of_api_key(message.api_key)[0]
            print(message.id)
            print(type(message.id))
            message.from_userid = f'{database.get_user_name_by_id(message.id)}#{message.id}'
            if not database.check_user(receiver_id):
                # send back that the user does not exist or his account is not activated and return
                print('User does not exist')
                return
            if database.is_authenticated(receiver_id):
                return
            if not database.is_online(receiver_id):
                print('Receiver is currently not online try again later!')
                return
            if not database.check_api_key(message.id, message.api_key):
                print(f'{message.from_userid} send message with invalid api key')
                print(message.api_key)
                return
            if not database.get_user_of_api_key(message.api_key)[0] == message.id:
                # TODO: Check if all get_user_of_api_key() only return the user part that they should
                api_key_id = database.get_user_of_api_key(message.api_key)
                print('API-KEY ID: ', api_key_id)
                print('User provided id: ', message.id)
                print('Userid and api key do not match')
                return
            receiver_ip = database.get_ip_of_user(receiver_id)
            sender: dict = database.get_user_of_api_key(message.api_key)
            # sock.sendto('Message Received. Forwarding...'.encode('utf-8'), self.client_address)
            receiver_pub_key = database.get_public_key_of_user(receiver_id)
            if not database.is_online(receiver_id):
                sock.sendto('receiver not online'.encode('utf-8'),
                            self.client_address)
                return
            else:
                forwarding_message = models.ForwardingClassicMessage(message, sender[0])
                fwdmessage = str(forwarding_message)
                sock.sendto(crypt.encrypt(fwdmessage, receiver_pub_key), receiver_ip)
                print(f'{sender[2]} »»» {database.get_user_name_by_id(receiver_id)}')

        elif message.message_type == models.MessageType.LoginMessage:
            message: models.LoginMessage
            message.ip = self.client_address  # type: ignore

            # if database.is_online(message.id):
            #    current_ip = database.get_ip_of_user(message.id)
            #    receiver_pub_key = rsa.PublicKey.load_pkcs1(database.get_public_key_of_user(
            #        message.id)[0])
            #    sock.sendto(crypt.encrypt(data=json.dumps({'Exception': 'NewUserLogin'}),
            #                              public_key=receiver_pub_key),
            #                current_ip)
            #    return
            if not f'{database.get_user_name_by_id(message.id)}#{message.id}' == message.userid:
                sock.sendto(crypt.encrypt(data=json.dumps({'Exception': 'Wrong UserID'}),
                                          public_key=message.client_public_key),
                            message.ip)
                print(f'{message.ip[0]}:{message.ip[1]} tried to log in with not matching '
                      f'username and id pair: {message.userid}')
                return
            if not database.check_password(message.id, message.hashed_password):
                sock.sendto(crypt.encrypt(data=json.dumps({'Exception': 'Wrong Password'}),
                                          public_key=message.client_public_key),
                            message.ip)
                print(f'{message.userid} tried to login with wrong password. On {message.ip[0]}:'
                      f'{message.ip[1]}')
                return


            database.set_online(message.id, message.ip, message.client_public_key)
            api_key = database.generate_api_key(message.id)
            sock.sendto(crypt.encrypt(data=api_key, public_key=message.client_public_key),
                        message.ip)
            print(f'{message.userid} just logged in from {message.ip[0]}:{message.ip[1]}')
        elif message.message_type == models.MessageType.LogoutMessage:
            message: models.LogoutMessage
            message.ip = self.client_address
            print(message.api_key)
            user = database.get_user_of_api_key(message.api_key)
            id = user[0]
            username = user[1]
            userid = user[2]
            print(f'Logging out {userid}')

            database.set_offline(id)

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

        elif message.message_type == models.MessageType.NoneMessage:
            print('None Message')

        # print(f'{self.client_address[0]} wrote: {data}')
        # sock.sendto(data.upper(), self.client_address)


if __name__ == '__main__':
    HOST, PORT = '127.0.0.1', 9999

    with socketserver.UDPServer((HOST, PORT), UDPHandler) as server:
        server.serve_forever()
