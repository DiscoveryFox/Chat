import rsa


# KEY_SIZE = 2048
# PUBLIC_EXP = 65537
# private_key = rsa.generate_private_key(
#     public_exponent=PUBLIC_EXP,
#     key_size=KEY_SIZE,
#     backend=default_backend()
# )
#
# private_key_str = private_key.private_bytes(
#     encoding=serialization.Encoding.PEM,
#     format=serialization.PrivateFormat.TraditionalOpenSSL,
#     encryption_algorithm=serialization.NoEncryption()
# ).decode()
#
# public_key = private_key.public_key()
# public_key_str = public_key.public_bytes(
#     encoding=serialization.Encoding.PEM,
#     format=serialization.PublicFormat.SubjectPublicKeyInfo,
# ).decode()

def gen_new_keys(database, key_length: int = 2048):
    publicKey, privateKey = rsa.newkeys(key_length)
    database.update_crypt_keys(publicKey, privateKey)


def load_crypt_keys(database):
    return database.get_crypt_keys()


def key_to_str(key):
    return key.save_pkcs1('PEM')


def load_key(str_key):
    return rsa.key.PublicKey.load_pkcs1(str_key)


def encrypt(data: str, public_key, encoding: str = 'utf-8') -> bytes:
    result: list = []
    if isinstance(public_key, tuple):
        if isinstance(public_key[0], (bytes, str)):
            public_key = rsa.PublicKey.load_pkcs1(public_key[0])
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
