from collections import Counter

import matplotlib.pyplot as plt


def validate_string(s: str):
    if s.lower() != s:
        raise RuntimeError("input must only contain lowercase characters")

    if not s.isalnum():
        raise RuntimeError("input must only contain alphanumeric characters (a-z)")


def shift_encrypt(pt: str, key: int) -> str:
    """Encrypt a string with the shift cipher.

    The string must only contain lowercase letters of the English
    alphabet. No spaces or symbols are allowed in the input.

    :param pt: the string to encrypt
    :param key: the shift
    :return: the encrypted message
    """
    validate_string(pt)
    ct: str = ""
    # Let pos be the 0-indexed position in the alphabet of some character 'c'.
    # Then each letter is encrypted separately with
    # (pos('c') + key) % 26
    # where 'pos()' computes the 0-indexed position of the letter in the
    # English alphabet.

    # The ASCII encodings do not begin at 0, so first we need the position
    # in the ASCII table: ord(c) - ord('a'), then we encrypt, and then we
    # adjust the output to be in the ASCII table with + ord('a') again.
    for c in pt:
        ct += chr(ord('a') + ((ord(c) - ord('a') + key) % 26))

    return ct


def shift_decrypt(ct: str, key: int) -> str:
    """Decrypt a ciphertext string with the shift cipher.

    The ciphertext must only contain lowercase letters of the English
    alphabet. No spaces or symbols are allowed in the input.

    :param ct: the ciphertext to decrypt
    :param key: the shift
    :return: the decrypted message
    """
    validate_string(ct)
    pt: str = ""
    # For decryption, we first also need the position in the alphabet.
    # Finally, we convert the result back to the ASCII table position.
    for c in ct:
        pt += chr(ord('a') + ((ord(c) - ord('a') - key) % 26))

    return pt


def shiftb_encrypt(pt: bytes, key: int) -> bytes:
    """Encrypt a byte string with the shift cipher.

    :param pt: the bytes to encrypt
    :param key: the shift
    :return: the encrypted bytes
    """

    # Bytes are just integers 0 <= x < 256, so we can have a list of
    # integers which we later convert to an immutable bytes object.
    # Implementation details really are annoying...
    ct: list[int] = []
    # The largest byte value is 255, so you can think of the alphabet as
    # bytes 0--255. We no longer care about encoding (functions take care of
    # that), so we can just apply the mod operator.
    for b in pt:
        ct.append((b + key) % 256)

    return bytes(ct)


def shiftb_decrypt(ct: bytes, key: int) -> bytes:
    """Decrypt a ciphertext with the shift cipher.

    :param ct: the ciphertext to decrypt
    :param key: the shift
    :return: the decrypted bytes
    """
    pt: list[int] = []
    for b in ct:
        pt.append((b - key) % 256)

    return bytes(pt)


def freq(message: str, msg_type: str):
    """Print the letter frequency diagram of a message.

    :param message: the message to get the frequencies for
    :param msg_type: the type of the message, e.g. plain or cipher
    """
    c = Counter(message)
    plt.bar(*zip(*c.most_common()), width=.5, color="g")
    plt.title(f"Letter frequencies of the {msg_type}")
    plt.show()


def main():
    message = "helloworld"
    key = 20

    ct = shift_encrypt(message, key)
    print(f"CT: {ct}")

    freq(ct, "ciphertext")

    pt = shift_decrypt(ct, key)
    print(f"PT: {pt}")

    freq(pt, "plaintext")

    # We now let the computer handle the encoding/decoding instead of manually
    # fiddling with alphabets/encoding.

    message = "Hello World! ✨"

    ct = shiftb_encrypt(message.encode("utf-8"), key)
    print(f"BCT: {ct.hex(' ').upper()}")

    pt = shiftb_decrypt(ct, key)
    print(f"BPT: {pt.decode('utf-8')}")


if __name__ == "__main__":
    main()
