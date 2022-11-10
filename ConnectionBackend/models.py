import hashlib
import socket
import json

import rsa


# noinspection DuplicatedCode
def encrypt(data: str, public_key, encoding: str = 'utf-8') -> bytes:
    result: list = []
    for n in range(0, len(data), 245):
        part = data[n:n + 245]
        result.append(rsa.encrypt(part.encode(encoding), public_key))
    return b''.join(result)


def decrypt(data: bytes, private_key, encoding: str = 'utf-8') -> str:
    result: list = []
    for n in range(0, len(data), 256):
        part = data[n:n + 256]
        decrypted_part = rsa.decrypt(part, private_key).decode(encoding)
        result.append(decrypted_part)
    return ''.join(result)


class MessageType:
    LoginMessage: str = 'LoginMessage'
    RegisterMessage: str = 'RegisterMessage'
    ClassicMessage: str = 'ClassicMessage'
    MultimediaMessage: str = 'MultimediaMessage'
    ServePublicKey: str = 'ServePublicKey'
    LogoutMessage: str = 'LogoutMessage'


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
                 userid: str | None = None,
                 hashed_password: str | None = None,
                 password: str | None = None):
        self.api_key = None
        self.sock: socket.SocketType = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.ip = ip
        self.client_public_key = client_public_key
        if self.client_public_key is None:
            self.client_public_key, self.client_private_key = rsa.newkeys(2048)
        if server_public_key is None:
            self.sock.sendto(bytes('04{}', 'utf-8'), ip)
            key_str = self.sock.recv(1024)
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
            'hashed_password': hashed_password,
            'client_public_key': self.client_public_key.save_pkcs1().decode('utf-8')
        }
        login_request_serialized = '01' + json.dumps(login_request)
        self.send_data(login_request_serialized)
        response = decrypt(self.sock.recv(1024), self.client_private_key)
        if response == '01User is already logged in.':
            pass
        else:
            self.api_key = response

        print(self.api_key)

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
            crypt_data: bytes = encrypt(data, self.server_public_key)
            self.sock.sendto(crypt_data, self.ip)
        else:
            self.sock.sendto(data.encode(encoding), self.ip)

    def send_message(self, message: str, receiver: str):

        ...
