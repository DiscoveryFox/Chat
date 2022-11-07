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
    pass


class RegisterMessage:
    pass


class ClassicMessage:
    SendTime    : float
    Text        : float
    To          : str
    MessageType: str



class MultimediaMessage:
    pass


class BaseMessage:
    SendTime: float
    Text: str
    To: str
    MessageType: str

    def __init__(self, message: bytes, encoding: str = 'utf-8'):
        self.SIGN_BYTES: dict = {
            0o0: self.register,
            0o1: self.login,
            0o2: self.message,
        }
        self.message: str = message.decode(encoding)

        self.sign_byte = int(self.message[:2])
        self.message = message[2:]

        try:
            self.message: dict = json.loads(self.message)
        except json.JSONDecodeError as JsonError:
            print('JSONDecodeError in line 10 with string: ')
            print('-------------')
            print(f'Sign Byte: {self.sign_byte}')
            print(self.message)
            print('-------------')
            raise JsonError

        self.SIGN_BYTES[self.sign_byte](self.message)

    def __new__(cls, *args, **kwargs):
        return

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
