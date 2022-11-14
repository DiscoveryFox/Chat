# pyright: reportGeneralTypeIssues=false
import socket
import json
from dataclasses import dataclass

import rsa

'''
message: dict = {
    'Message': 'Actual Message as String',
    'SendTime': datetime object,
    'From': Username,
    'To': Username
}
'''


@dataclass
class MessageType:
    LoginMessage: str = 'LoginMessage'
    RegisterMessage: str = 'RegisterMessage'
    ClassicMessage: str = 'ClassicMessage'
    MultimediaMessage: str = 'MultimediaMessage'
    ServePublicKey: str = 'ServePublicKey'
    LogoutMessage: str = 'LogoutMessage'
    ForwardingClassicMessage: str = 'ForwardingClassicMessage'
    NoneMessage: str = 'NoneMessage'


class UserAlreadyExists(Exception):
    def __init__(self, username: str):
        self.username = username

    def __str__(self):
        return f'{self.username} already exists!'


class LoginMessage:
    message_type: str = MessageType.LoginMessage
    ip: tuple
    userid: str
    hashed_password: str

    def __init__(self, data):
        self.userid = data['UserID']
        self.id = self.userid.split('#')[1]
        self.hashed_password = data['Password']
        self.client_public_key = rsa.PublicKey.load_pkcs1(data['client_public_key'].encode('utf-8'))
        self.ip: tuple | None = None


class LogoutMessage:
    message_type: str = MessageType.LogoutMessage
    ip = tuple
    api_key: str

    def __init__(self, data):
        self.api_key = data['api_key']


class ServePublicKey:
    message_type: str = MessageType.ServePublicKey

    def __init__(self):
        self.ip: tuple = (None, None)


class NoneMessage:
    message_type: str = MessageType.NoneMessage

    def __init__(self, data):
        ...


class RegisterMessage:
    message_type: str = MessageType.RegisterMessage

    def __init__(self, data):
        ...


class ClassicMessage:
    send_time: float
    text: str
    to: str
    api_key: str

    message_type: str = MessageType.ClassicMessage

    def __init__(self, data):
        self.text = data['Message']
        self.send_time = data['SendTime']
        self.api_key = data['ApiKey']
        self.to = data['To']
        self.from_userid: str = data['From']
        self.id = self.from_userid.split('#')[1]

    def toJson(self):
        return json.dumps(self.__dict__)


class ForwardingClassicMessage:
    message_type = MessageType.ForwardingClassicMessage

    def __init__(self, message: ClassicMessage, from_id: int):
        self.text = message.text
        self.sender = from_id
        self.send_time = message.send_time

    def __str__(self):
        return json.dumps(self.__dict__)

    def toJson(self):
        return json.dumps(self.__dict__)


class MultimediaMessage:
    send_time: float
    to: str
    contentlink: str
    message_type: str = MessageType.MultimediaMessage

    def __init__(self, data):
        ...


class BaseMessage:
    message_type: str = 'BaseMessage'
    SIGN_BYTES: dict = {
        0o0: MessageType.RegisterMessage,
        0o1: MessageType.LoginMessage,
        0o2: MessageType.ClassicMessage,
        0o3: MessageType.MultimediaMessage,
        0o4: MessageType.ServePublicKey,
        0o5: MessageType.LogoutMessage,
        0o6: MessageType.NoneMessage
    }

    def __new__(cls, data, private_key, encoding='utf-8', *args, **kwargs):
        try:
            sign_byte = int(data[:2])
            return ServePublicKey
        except ValueError:
            pass
        result: list = []
        try:
            for n in range(0, len(data), 256):
                part = data[n:n + 256]
                try:
                    decrypted_part = rsa.decrypt(part, private_key).decode('utf-8')
                except rsa.pkcs1.DecryptionError as crypt_error:
                    print('DecryptionError')
                    print(part)
                    continue
                result.append(decrypted_part)
        except rsa.DecryptionError as De:
            raise De
        data: str = ''.join(result)
        # data: str = rsa.decrypt(data, private_key).decode('utf-8')

        try:
            if not data == '':
                sign_byte = int(data[:2])
            else:
                return NoneMessage(data1)
        except ValueError as Ve:
            print('Decryption Error: ')
            print(data)
            print('-----------------')
            raise Ve

        if BaseMessage.SIGN_BYTES[sign_byte] == MessageType.ServePublicKey:
            print('ServePublicKey')
            return ServePublicKey()
        message: str = data[2:]
        data: dict = json.loads(message)
        message_type = BaseMessage.SIGN_BYTES[sign_byte]
        match message_type:
            case MessageType.RegisterMessage:
                return RegisterMessage(data)
            case MessageType.LoginMessage:
                return LoginMessage(data)
            case MessageType.ClassicMessage:
                return ClassicMessage(data)
            case MessageType.MultimediaMessage:
                return MultimediaMessage(data)
            case MessageType.LogoutMessage:
                return LogoutMessage(data)
            case _:
                return NotImplemented
