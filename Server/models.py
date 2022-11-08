# pyright: reportGeneralTypeIssues=false
import socket
import json
from dataclasses import dataclass

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
        self.userid = data['userid']
        self.hashed_password = data['hashed_password']
        self.ip: tuple | None = None

class RegisterMessage:
    message_type: str = MessageType.RegisterMessage

    def __init__(self, data):
        ...


class ClassicMessage:
    send_time: float
    text: float
    to: str
    message_type: str = MessageType.ClassicMessage

    def __init__(self, data):
        self.text = data['Message']
        self.send_time = data['SendTime']
        self.sender = data['From']
        self.to = data['To']


class MultimediaMessage:
    SendTime: float
    To: str
    ContentLink: str
    message_type: str = MessageType.MultimediaMessage

    def __init__(self, data):
        ...


class BaseMessage:
    message_type: str = 'BaseMessage'
    SIGN_BYTES: dict = {
        0o0: MessageType.RegisterMessage,
        0o1: MessageType.LoginMessage,
        0o2: MessageType.ClassicMessage,
        0o3: MessageType.MultimediaMessage
    }

    def __new__(cls, data, encoding='utf-8', *args, **kwargs):
        data: str = data.decode(encoding)
        sign_byte = int(data[:2])
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
            case _:
                return NotImplemented
