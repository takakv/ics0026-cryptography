from Crypto.Cipher import AES
from Crypto.Hash import SHAKE128
from Crypto.Protocol.DH import key_agreement
from Crypto.PublicKey import ECC
from Crypto.Util.Padding import pad


def kdf(s: bytes, keylen: int = 16):
    """Derive a secret from the seed.

    :param s: The KDF seed
    :param keylen: The length of the desired secret
    :return: the derived secret
    """
    return SHAKE128.new(s).read(keylen)


def main():
    with open("p384_pub.pem", "rt") as f:
        data = f.read()
        server_pk = ECC.import_key(data)

    user_static = ECC.generate(curve="p384")
    user_ephemeral = ECC.generate(curve="p384")

    print(user_static.public_key().export_key(format="PEM"))
    print(user_ephemeral.public_key().export_key(format="PEM"))

    session_key = key_agreement(static_priv=user_static,
                                static_pub=server_pk,
                                eph_priv=user_ephemeral,
                                kdf=kdf)

    message = "It's dangerous to go alone! Take this. 🗡️".encode("utf-8")

    cipher = AES.new(session_key, AES.MODE_CBC)
    iv = cipher.iv
    ct = cipher.encrypt(pad(message, AES.block_size))

    print(ct.hex())
    print(iv.hex())


if __name__ == "__main__":
    main()
