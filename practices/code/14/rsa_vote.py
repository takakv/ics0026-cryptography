import secrets
from hashlib import shake_128

from Crypto import Hash
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

ELECTION_PARAMETERS = {
    "election_id": "hkyu24",
    "election_question": "Who is your favourite Karasuno High player?",
    "candidates": ["Daichi Sawamura", "Kōshi Sugawara", "Asahi Azumane", "Yū Nishinoya", "Ryūnosuke Tanaka",
                   "Tobio Kageyama", "Shōyō Hinata", "Kei Tsukishima", "Tadashi Yamaguchi"],
    "public_key": """-----BEGIN PUBLIC KEY-----
MIIBojANBgkqhkiG9w0BAQEFAAOCAY8AMIIBigKCAYEA7Aq3Rf7Unk/t3+jBY3ON
gyRofW4qFP/jR3wKwR1iBGTbvYD6Uz7H41ejPRqn9AcEojUFGl6YEXDDvhzOtumU
zOgI021u/1vbdoJfYEUGKzH99iv2eNyO3T8tbG3oO9BjFqAbBD5zzkbsCABfkD79
5DCUtZy03h5vfosVtPCqRXPhqQcPzvUqxngMC6Hl4/E8r7oxF7kcIjrwZWsHaJw3
PgSthizwlfvHckbjqUL6/aqdoGSTegZvTQr+nLl12xlFlK9LErd+8KB9fjT9j/WI
Yq7mc1S846Fc/q+iZFamJtFgM207H9U9D9Gk9UuEkVDM5iRVlWGtRb68xy3QJ3eC
7cmjDmA6/QjsfwXCkmwwtIshulHNzXBE71eH7ny989QQln7TXb+ilfcZ54N8DtaN
Gh42PbsGAbDIlHnxNAwfgipnUU1l6DXchWqJYi8h99X7Zdz36aOOh30o1gsdWsKw
YDezZ0SHKb8t+18Pp97T3QDBv+iOz9r7yn4wkgKQNIc5AgMBAAE=
-----END PUBLIC KEY-----"""
}


class CSPRNG:
    """Class to represent a cryptographic PRNG with a programmable seed.

    This is needed to be able to present the encryption randomness to the
    ‘verification application’.
    """

    def __init__(self, seed: bytes = secrets.token_bytes(16)) -> None:
        self._seed = seed

    @property
    def seed(self) -> bytes:
        return self._seed

    def token_bytes(self, n: int) -> bytes:
        """Get pseudo random bytes.

        :param n: the number of bytes to get.
        :return: the pseudo random bytes.
        """
        return shake_128(self._seed).digest(n)


VERIFICATION_INFO = {
    "encryption_randomness": "92d0038ddd940817cec28bb2cc961bb5",
    "ciphertext": "e99b018c00cb1562cd0e26fa7ff9cc77c38d92ff939e796758505c9f687ce8b45b6e637f42060718c5235e3f04cca4c84524554956cfd5ead84aa46ca1e7073659cb7ab43a42d06335edc5034b100be1907091347d2214a67e22b3c895c82a51b6b2806962a94819fe92cc43382f27e36a9afcdaabf3de911cbbb224fcceb622799560bdff42d1b8c05660eeb66c251613e69e32f279e194f06692d19e690a0cab09860f49e188e08a3415a03806a938a8fdc1dcdd1ee1977a9b2541743cc5296bf8a3c3839bb7652c44efc503db426febd8dfc8169aee4a4697cca6157db29ff84139b4dde77e264fcfd768ba8b1f050ca343da613e0b803bc9d18ac7604e014168f26625dae247efffb3414f082b49a68ff488c49807bd0d82509e90e559c65fe763cd5aa1b656b0348490c93162ac6b1d3bed8aa061877ac722b60c105cc586a777164fdf2a3dcf59546f0b716c53657c51fc757094a0eaac37191e312e710c34c01c481b71f7a14401e6bdc31ca49815079804ce35a7374effcb8069ad5f"
}


def vote_encryption(m: str) -> tuple[bytes, bytes]:
    """Encrypt a vote for the specified candidate.

    In addition to the ciphertext, the encryption randomness is returned
    in order for the voter to verify their vote with the independent
    verification application.

    :param m: the candidate to vote for
    :return: the encrypted vote and the encryption randomness.
    """
    pk = RSA.importKey(ELECTION_PARAMETERS["public_key"])
    prng = CSPRNG()
    cipher = PKCS1_OAEP.new(pk, hashAlgo=Hash.SHA256, randfunc=prng.token_bytes)
    ciphertext = cipher.encrypt(m.encode())
    return ciphertext, prng.seed


def main():
    pk = RSA.importKey(ELECTION_PARAMETERS["public_key"])
    ...


if __name__ == "__main__":
    main()
