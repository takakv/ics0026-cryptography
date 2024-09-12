import base64
import json
from base64 import b64encode
from wsgiref.util import request_uri

from Crypto.Cipher import ChaCha20
from Crypto.Random import get_random_bytes

# Do not use this to cheat!
SECRET_KEY = bytes.fromhex("fb8bfe0dc4f766eb5f2484e30b59b6682e804bfdf2d4c1e3dbff91d6acf52302")


def encrypt(pt: bytes, nonce: bytes = get_random_bytes(8)) -> tuple[bytes, bytes]:
    """Encrypt the provided plaintext.

    If no nonce is provided, a random nonce is used.
    :param pt: the plaintext to encrypt
    :param nonce: the nonce to use
    :return: a tuple [ciphertext, nonce]
    """
    cipher = ChaCha20.new(key=SECRET_KEY, nonce=nonce)
    ciphertext = cipher.encrypt(pt)
    return ciphertext, cipher.nonce


if __name__ == "__main__":
    challenge_pt = b""
    ct, nc = encrypt(challenge_pt)
    # lW02ZQZy0GjtwNkl3GZoGI/BT8aWJ5NGkULsYzu9FyMTFxcf8Q==
    print(base64.b64encode(ct).decode())
    # yU2Xdkx4Vqo=
    print(base64.b64encode(nc).decode())
