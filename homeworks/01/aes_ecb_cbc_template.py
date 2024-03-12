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


def encrypt(msg: bytes, key: bytes, iv: bytes = None) -> bytes:
    """Encrypt a message in CBC mode.

    If the IV is not provided, generate a random IV.
    :param msg: The message to encrypt
    :param key: The encryption key
    :param iv: The IV used for encryption
    :return: the ciphertext with the IV as the first block
    """
    pass


def decrypt(ct: bytes, key: bytes) -> bytes:
    """Decrypt a ciphertext in CBC mode.

    :param ct: The encrypted message
    :param key: The decryption key
    :return: the unpadded plaintext
    """
    pass


def encrypt_lib(msg: bytes, key: bytes, iv: bytes) -> bytes:
    """Encrypt a message using library CBC.

    :param msg: The message to encrypt
    :param key: The encryption key
    :param iv: The IV used for encryption
    :return: the ciphertext with the IV as the first block
    """
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    return iv + cipher.encrypt(pad_pkcs(msg))


def decrypt_lib(ct: bytes, key: bytes) -> bytes:
    """Decrypt a ciphertext using library CBC.

    :param ct: The encrypted message
    :param key: The decryption key
    :return: the unpadded plaintext
    """
    cipher = AES.new(key, AES.MODE_CBC)
    return unpad_pkcs(cipher.decrypt(ct)[BLOCK_SIZE:])


def main(i_key: str, i_msg: str, i_iv: str):
    key = ...
    msg = ...
    iv = ...

    ciphertext = encrypt(...)
    check_enc = encrypt_lib(msg, key, ciphertext[:BLOCK_SIZE])

    assert ciphertext == check_enc

    # Do not remove or modify the print statements.
    print("Key:", key.hex())
    print("PT :", msg.hex())
    print("IV :", ciphertext[:BLOCK_SIZE].hex())
    print("CT :", ciphertext[BLOCK_SIZE:].hex())

    decrypted = decrypt(...)
    check_dec = decrypt_lib(ciphertext, key)

    assert decrypted == check_dec
    assert decrypted == msg


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("key", help="the secret key")
    parser.add_argument("message", help="the message to encrypt")
    parser.add_argument("--iv", help="the initialisation vector (optional)")

    args = parser.parse_args()
    main(args.key, args.message, args.iv)
