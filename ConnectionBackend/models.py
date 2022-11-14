import hashlib
from pprint import pprint
import socket
import json
import time
import rsa


class MessageType:
    LoginMessage: str = 'LoginMessage'
    RegisterMessage: str = 'RegisterMessage'
    ClassicMessage: str = 'ClassicMessage'
    MultimediaMessage: str = 'MultimediaMessage'
    ServePublicKey: str = 'ServePublicKey'
    LogoutMessage: str = 'LogoutMessage'


class WrongPasswordError(Exception):
    ...

class ServerConnection:
    SIGN_BYTES: dict = {
        0o0: MessageType.RegisterMessage,
        0o1: MessageType.LoginMessage,
        0o2: MessageType.ClassicMessage,
        0o3: MessageType.MultimediaMessage,
        0o4: MessageType.ServePublicKey,
        0o5: MessageType.LogoutMessage
    }

    def __init__(self,
                 ip: tuple[str, int],
                 client_public_key: rsa.PublicKey | None = None,
                 server_public_key: rsa.PublicKey | None = None,
                 client_private_key: rsa.PrivateKey | None = None,
                 userid: str | None = None,
                 hashed_password: str | None = None,
                 password: str | None = None):
        self.api_key = None
        self.sock: socket.SocketType = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_ip = ip
        self.client_public_key = client_public_key
        self.client_private_key = client_private_key
        if self.client_public_key is None:
            self.client_public_key, self.client_private_key = rsa.newkeys(2048)
        if server_public_key is None:
            self.sock.sendto(bytes('04{}', 'utf-8'), ip)
            key_str = self.sock.recv(2048)
            self.server_public_key = rsa.key.PublicKey.load_pkcs1(key_str)
        else:
            self.server_public_key = server_public_key
        if hashed_password and password:
            clear_password_hashed = hashlib.blake2b(password.encode('utf-8')).hexdigest()
            assert hashed_password == clear_password_hashed
        if userid and hashed_password:
            self.login(userid, hashed_password)
        elif userid and password:
            password_hashed = hashlib.blake2b(password.encode('utf-8')).hexdigest()
            self.login(userid, password_hashed)

    def __enter__(self):
        ...

    def __exit__(self, exc_val, exc_tb):
        ...

    def login(self, userid: str, hashed_password: str):
        self.api_key: str
        login_request: dict = {
            'UserID': userid,
            'Password': hashed_password,
            'client_public_key': self.client_public_key.save_pkcs1().decode('utf-8')
        }
        login_request_serialized = '01' + json.dumps(login_request)
        self.send_data(login_request_serialized)
        response = self.decrypt(self.sock.recv(4096))
        if response == '01User is already logged in.':
            ...
        elif response == '{"Exception": "Wrong UserID"}':
            raise WrongPasswordError
        elif response == '{"Exception": "Wrong Password"}':
            raise WrongPasswordError
        else:
            self.api_key = response

    def _send_message(self, message, sign_byte):
        """
        :param message:
        :param sign_byte:
        :return:
        """
        ...

    def send_data(self, data: str, encrypted: bool = True, encoding: str = 'utf-8'):
        """
        :param data: str: The data that should be sent to the server.
        :param encrypted: bool: If the data should be encrypted before sending or not.
        :param encoding: str: The encoding for the String if you send data without encryption.
        :return: Nothing
        """
        if encrypted:
            crypt_data: bytes = self.encrypt(data)
            self.sock.sendto(crypt_data, self.server_ip)
        else:
            self.sock.sendto(data.encode(encoding), self.server_ip)

    def send_message(self, message: str, receiver: str, debug=False):
        message_struct = {
            'Message': message,
            'SendTime': time.time(),
            'ApiKey': self.api_key,
            'To': receiver,
            'From': 'flinnfx#1'
        }
        if debug is True:
            pprint(message_struct)
        self.send_data('02'+json.dumps(message_struct))

    def decrypt(self, data: bytes, encoding: str = 'utf-8') -> str:
        result: list = []
        for n in range(0, len(data), 256):
            part = data[n:n + 256]
            decrypted_part = rsa.decrypt(part, self.client_private_key).decode(encoding)
            result.append(decrypted_part)
        return ''.join(result)

    # noinspection DuplicatedCode
    def encrypt(self, data: str, encoding: str = 'utf-8') -> bytes:
        result: list = []
        for n in range(0, len(data), 245):
            part = data[n:n + 245]
            result.append(rsa.encrypt(part.encode(encoding), self.server_public_key))
        return b''.join(result)
