import argparse

from Crypto.Cipher import AES

BLOCK_SIZE = AES.block_size


def pad_pkcs(msg: bytes, bl: int = BLOCK_SIZE) -> bytes:
    """Pad a message to a multiple of the block length following PKCS#7.

    :param msg: The message to pad
    :param bl: The block length
    :return: the padded message
    """
    pass


def unpad_pkcs(padded: bytes, bl: int = BLOCK_SIZE) -> bytes:
    """Remove PKCS#7 message padding.

    :param padded: The padded message
    :param bl: The block length
    :return: the unpadded message
    """
    pass


def encrypt(msg: bytes, key: bytes, iv: bytes = None) -> tuple[bytes, bytes]:
    """Encrypt a message in CBC mode.

    If the IV is not provided, generate a random IV.
    :param msg: The message to encrypt
    :param key: The encryption key
    :param iv: The initialisation vector
    :return: a tuple (ciphertext, iv)
    """
    pass


def decrypt(ct: bytes, key: bytes, iv: bytes) -> bytes:
    """Decrypt a ciphertext in CBC mode.

    :param ct: The encrypted message
    :param key: The decryption key
    :param iv: The initialisation vector
    :return: the unpadded plaintext
    """
    pass


# Do not modify. Needed for code correctness assertions.
def encrypt_lib(msg: bytes, key: bytes, iv: bytes) -> bytes:
    """Encrypt a message using library CBC.

    :param msg: The message to encrypt
    :param key: The encryption key
    :param iv: The initialisation vector
    :return: the ciphertext
    """
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    return cipher.encrypt(pad_pkcs(msg))


# Do not modify. Needed for code correctness assertions.
def decrypt_lib(ct: bytes, key: bytes, iv: bytes) -> bytes:
    """Decrypt a ciphertext using library CBC.

    :param ct: The encrypted message
    :param key: The decryption key
    :param iv: The initialisation vector
    :return: the unpadded plaintext
    """
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    return unpad_pkcs(cipher.decrypt(ct))


def main(i_key: str, i_msg: str, i_iv: str):
    key = ...
    msg = ...
    iv = ...

    ciphertext, iv = encrypt(...)
    check_enc = encrypt_lib(msg, key, iv)

    assert ciphertext == check_enc

    # Do not remove or modify the print statements.
    print("Key:", key.hex())
    print("PT :", msg.hex())
    print("IV :", iv.hex())
    print("CT :", ciphertext.hex())

    decrypted = decrypt(...)
    check_dec = decrypt_lib(ciphertext, key, iv)

    assert decrypted == check_dec
    assert decrypted == msg


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("key", help="the secret key")
    parser.add_argument("message", help="the message to encrypt")
    parser.add_argument("--iv", help="the initialisation vector (optional)")

    args = parser.parse_args()
    main(args.key, args.message, args.iv)
