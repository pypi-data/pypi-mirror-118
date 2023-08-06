##  @packege zeus_security_py
#   Helper package for data security that will implement zeus microservices
#
#
from Cryptodome.Cipher import AES
from Cryptodome import Random
from hashlib import sha256
import base64
import os
import json

__author__ = "Noé Cruz | contactozurckz@gmail.com"
__copyright__ = "Copyright 2007, The Cogent Project"
__credits__ = ["Noé Cruz", "Zurck'z", "Jesus Salazar"]
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Noé Cruz"
__email__ = "contactozurckz@gmail.com"
__status__ = "Dev"

##  Class Encryptor
#   Encryptor class contains AES encrypt/decrypt functions
#
class AESEncryptor:
    """
    Helper class for data security this contains certain methods for it.

    AES (Advanced Encryption Standard) is a symmetric block cipher standardized by NIST .
    It has a fixed data block size of 16 bytes. Its keys can be 128, 192, or 256 bits long.

    Attributes
    ----------
    default_block_size : int
        Default block size for aes (default 32)
    _sk_env : str
        Key for get secret key from environment

    Methods
    -------
    __is_valid(sk=None)
        Check if the secret key of argument is null, if that is null try to get secret key from environment.
    encrypt
    """

    default_block_size: int = 32
    _sk_env = "AES_SK"

    @staticmethod
    def __is_valid(sk: str = None):
        if sk is not None:
            return sk
        sk_env: str = os.getenv(AESEncryptor._sk_env)
        if sk_env is not None:
            return sk_env
        raise Exception("AES Secret key was not provided!")

    @staticmethod
    def decrypt_ws_response(payload: dict, secret_key=None) -> dict:
        json_decrypted = AESEncryptor.decrypt(payload["data"], secret_key)
        return json_decrypted

    @staticmethod
    def encrypt_ws_request(payload: dict, secret_key=None) -> dict:
        encrypted_payload = AESEncryptor.encrypt(json.dumps(payload), secret_key)
        return {"data": encrypted_payload}

    @staticmethod
    def json_decrypt(json_encrypted: str, secret_key=None) -> dict:
        return json.loads(AESEncryptor.encrypt(json_encrypted, secret_key))

    @staticmethod
    def json_encrypt(json_to_encrypt: dict, secret_key=None) -> str:
        json_str = json.dumps(json_to_encrypt)
        return AESEncryptor.encrypt(json_str, secret_key)

    @staticmethod
    def json_decrypt(json_encrypted: str, secret_key=None) -> dict:
        return json.loads(AESEncryptor.encrypt(json_encrypted, secret_key))

    @staticmethod
    def encrypt(
        value: str,
        secret_key: str = None,
        aes_mode=AES.MODE_CBC,
        charset="utf-8",
        block_size: int = 16,
    ) -> str:
        secret_key = AESEncryptor.__is_valid(secret_key).encode(charset)
        raw_bytes = AESEncryptor.__pad(value)
        iv = Random.new().read(block_size)
        cipher = AES.new(secret_key, aes_mode, iv)
        return base64.b64encode(iv + cipher.encrypt(raw_bytes)).decode(charset)

    @staticmethod
    def decrypt(
        value: str, secret_key=None, aes_mode=AES.MODE_CBC, charset="utf-8"
    ) -> str:
        secret_key = str.encode(AESEncryptor.__is_valid(secret_key))
        encrypted = base64.b64decode(value)
        iv = encrypted[:16]
        cipher = AES.new(secret_key, aes_mode, iv)
        return AESEncryptor.__un_pad(cipher.decrypt(encrypted[16:])).decode(charset)

    @staticmethod
    def genHash(value: str, charset="utf-8") -> str:
        return sha256(value.encode(charset)).hexdigest()

    @staticmethod
    def __pad(s: str, block_size: int = 16, charset: str = "utf-8") -> bytes:
        return bytes(
            s
            + (block_size - len(s) % block_size)
            * chr(block_size - len(s) % block_size),
            charset,
        )

    @staticmethod
    def __un_pad(value: str) -> str:
        return value[0 : -ord(value[-1:])]
