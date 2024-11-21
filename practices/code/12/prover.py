import secrets
from collections import namedtuple
from hashlib import shake_128

from gmpy2 import gmpy2
from pyasn1_modules.rfc5958 import PublicKey

RFC3526_3072_HEX = """FFFFFFFF FFFFFFFF C90FDAA2 2168C234 C4C6628B 80DC1CD1
      29024E08 8A67CC74 020BBEA6 3B139B22 514A0879 8E3404DD
      EF9519B3 CD3A431B 302B0A6D F25F1437 4FE1356D 6D51C245
      E485B576 625E7EC6 F44C42E9 A637ED6B 0BFF5CB6 F406B7ED
      EE386BFB 5A899FA5 AE9F2411 7C4B1FE6 49286651 ECE45B3D
      C2007CB8 A163BF05 98DA4836 1C55D39A 69163FA8 FD24CF5F
      83655D23 DCA3AD96 1C62F356 208552BB 9ED52907 7096966D
      670C354E 4ABC9804 F1746C08 CA18217C 32905E46 2E36CE3B
      E39E772C 180E8603 9B2783A2 EC07A28F B5C55DF0 6F4C52C9
      DE2BCBF6 95581718 3995497C EA956AE5 15D22618 98FA0510
      15728E5A 8AAAC42D AD33170D 04507A33 A85521AB DF1CBA64
      ECFB8504 58DBEF0A 8AEA7157 5D060C7D B3970F85 A6E1E4C7
      ABF5AE8C DB0933D7 1E8C94E0 4A25619D CEE3D226 1AD2EE6B
      F12FFA06 D98A0864 D8760273 3EC86A64 521F2B18 177B200C
      BBE11757 7A615D6C 770988C0 BAD946E2 08E24FA0 74E5AB31
      43DB5BFC E0FD108E 4B82D120 A93AD2CA FFFFFFFF FFFFFFFF"""

Ciphertext = namedtuple("Ciphertext", ["u", "v"])
Commitment = namedtuple("Commitment", ["mc", "kc"])
Transcript = namedtuple("Transcript", ["commitment", "challenge", "response"])


def byte_length(i):
    return (i.bit_length() + 7) // 8


# INSECURE! Learning purposes only. Do not use in production systems!
class PublicKey:
    def __init__(self, pk: int):
        self.p = int.from_bytes(bytes.fromhex(RFC3526_3072_HEX), "big")
        self.q = (self.p - 1) // 2
        self.g = 2

        self.pk = pk

    def encrypt(self, m: int) -> Ciphertext:
        """Encrypt a message.

        :param m: The message to encrypt
        :return: the ElGamal ciphertext
        :raises ValueError: If the message is too large or too small
        """
        if not 1 <= m < self.q:
            raise ValueError("Message not suitable for encryption")

        # We need this to work in the group of quadratic residues.
        if gmpy2.legendre(m, self.p) != 1:
            m = self.p - m

        r = secrets.randbelow(self.q)
        u = gmpy2.powmod_sec(self.g, r, self.p)

        blind = gmpy2.powmod_sec(self.pk, r, self.p)
        v = (m * blind) % self.p

        return Ciphertext(u, v)


def fiatshamir(ct: Ciphertext, m: int, pk: PublicKey, commitment: Commitment) -> int:
    bl = byte_length(pk.pk)

    seed = b""
    seed += ct.u.to_bytes(bl, byteorder="big")
    seed += ct.v.to_bytes(bl, byteorder="big")
    seed += m.to_bytes(byte_length(m), byteorder="big")
    seed += pk.g.to_bytes(bl, byteorder="big")
    seed += pk.p.to_bytes(bl, byteorder="big")
    seed += commitment.mc.to_bytes(bl, byteorder="big")
    seed += commitment.kc.to_bytes(bl, byteorder="big")

    return int.from_bytes(shake_128(seed).digest(bl - 1), "big")


# INSECURE! Learning purposes only. Do not use in production systems!
class SecretKey:
    def __init__(self):
        self.p = int.from_bytes(bytes.fromhex(RFC3526_3072_HEX), "big")
        self.q = (self.p - 1) // 2
        self.g = 2

        self._sk = secrets.randbelow(self.q)

        pk = gmpy2.powmod_sec(self.g, self._sk, self.p)
        self._pk = PublicKey(pk)

    def provable_decrypt(self, ct: Ciphertext) -> tuple[int, Transcript]:
        """Provably decrypt an ElGamal ciphertext.

        :param ct: The ciphertext to decrypt
        :return: the decrypted message and the transcript
        """
        # Ensure that the ciphertext components are quadratic residues.
        assert gmpy2.legendre(ct.u, self.p) == 1
        assert gmpy2.legendre(ct.v, self.p) == 1
        # Sanity check.
        assert ct.u < self.p and ct.v < self.p

        sk_minus = (0 - self._sk) % self.q
        message = gmpy2.powmod_sec(ct.u, sk_minus, self.p)
        message = (ct.v * message) % self.p

        # Convert group element back to an integer.
        if message > self.q:
            message = self.p - message

        rand = secrets.randbelow(self.q)
        msg_comm = gmpy2.powmod_sec(ct.u, rand, self.p)
        key_comm = gmpy2.powmod_sec(self.g, rand, self.p)

        commitment = Commitment(int(msg_comm), int(key_comm))

        challenge = fiatshamir(ct, message, self.pk, commitment)
        response = (challenge * self._sk + rand) % self.q

        transcript = Transcript(commitment, challenge, response)
        return message, transcript

    @property
    def pk(self):
        return self._pk


def main():
    sk = SecretKey()
    pk = sk.pk

    m = 7

    ct = pk.encrypt(m)

    dec, proof = sk.provable_decrypt(ct)

    assert dec == m

    print("Public key:")
    print(pk.pk)
    print()

    print("u:")
    print(int(ct.u))
    print("v:")
    print(int(ct.v))

    print(proof)


if __name__ == "__main__":
    main()
