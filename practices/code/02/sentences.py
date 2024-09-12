import secrets


def xor(a: bytes, b: bytes):
    return bytes(c ^ d for (c, d) in zip(a, b))


def generate():
    messages = [b"This task is very cool!",
                b"Cryptography is awesome",
                b"What is the correct key",
                b"The practice is hard :("]

    l = len(messages[0])

    ciphertext = secrets.token_bytes(l)

    keys: list[bytes] = []
    for m in messages:
        keys.append(xor(m, ciphertext))

    print(ciphertext.hex().upper())
    print([f"{key.hex().upper()}" for key in keys])


def solve():
    key_strings = ["BA1982AE0FFCF3496A35D85DAAC3993506DF10E625DE7A",
                   "AD0392AD5BE7F5486065D957AADC8F671E8816FA25DF3E",
                   "B9198AA90FE1E11A757DD40EE9DA8E351A9C07A921D722",
                   "BA198EFD5FFAF359757CD24BAADC8F67179E01ED6A8873"]
    keys = [bytes.fromhex(k) for k in key_strings]

    ciphertext = "EE71EBDD2F88923A0115B12E8AB5FC477FFF73894AB25B"
    ct_bytes = bytes.fromhex(ciphertext)

    for k in keys:
        print(xor(ct_bytes, k).decode())


if __name__ == "__main__":
    # generate()
    solve()
