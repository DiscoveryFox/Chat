import socket
import json

'''
message: dict = {
    'Message': 'Actual Message as String',
    'SendTime': datetime object,
    'From': Username,
    'To': Username
}
'''


class UserAlreadyExists(Exception):
    def __init__(self, username: str):
        self.username = username

    def __str__(self):
        return f'{self.username} already exists!'


class LoginMessage:
    MessageType: str = 'LoginMessage'

    def __init__(self, data):
        ...


class RegisterMessage:
    MessageType: str = 'RegisterMessage'

    def __init__(self, data):
        ...


class ClassicMessage:
    SendTime: float
    Text: float
    To: str
    MessageType: str = 'ClassicMessage'

    def __init__(self, data):
        self.Text = data['Message']
        self.SendTime = data['SendTime']
        self.From = data['From']
        self.To = data['To']


class MultimediaMessage:
    SendTime: float
    To: str
    ContentLink: str
    MessageType: str = 'MultimediaMessage'

    def __init__(self, data):
        ...


class BaseMessage:
    MessageType: str = 'BaseMessage'
    SIGN_BYTES: dict = {
        0o0: 'RegisterMessage',
        0o1: 'LoginMessage',
        0o2: 'ClassicMessage'
    }

    def __new__(cls, data, encoding='utf-8', *args, **kwargs):
        data: str = data.decode(encoding)
        sign_byte = int(data[:2])
        message: str = data[2:]
        data: dict = json.loads(message)
        MessageType = BaseMessage.SIGN_BYTES[sign_byte]
        match MessageType:
            case RegisterMessage.MessageType:
                return RegisterMessage(data)
            case LoginMessage.MessageType:
                return LoginMessage(data)
            case ClassicMessage.MessageType:
                return ClassicMessage(data)
            case _:
                return NotImplemented

    def login(self, data: dict):
        self.MessageType = 'LoginMessage'

    def message(self, data: dict):
        self.MessageType = 'ClassicalMessage'
        self.SendTime = data['SendTime']
        self.Text = data['Message']
        self.To = data['To']

    def register(self, data: dict):
        self.MessageType = 'RegisterMessage'
        self.Username = data['username']
        self.Email = data['email']
