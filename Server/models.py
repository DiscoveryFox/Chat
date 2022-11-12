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
    id: int

    def __init__(self, data):
        self.id = data['id']


class ServePublicKey:
    message_type: str = MessageType.ServePublicKey

    def __init__(self):
        self.ip: tuple = (None, None)


class RegisterMessage:
    message_type: str = MessageType.RegisterMessage

    def __init__(self, data):
        ...


class ClassicMessage:
    send_time: float
    text: float
    to: str
    api_key: str

    message_type: str = MessageType.ClassicMessage

    def __init__(self, data):
        self.text = data['Message']
        self.send_time = data['SendTime']
        self.api_key = data['ApiKey']
        self.to = data['To']


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
        0o5: MessageType.LogoutMessage
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
                print(decrypted_part)
        except rsa.DecryptionError as De:
            raise De
        data: str = ''.join(result)
        # data: str = rsa.decrypt(data, private_key).decode('utf-8')
        sign_byte = int(data[:2])
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
                return LogoutMessage
            case _:
                return NotImplemented
