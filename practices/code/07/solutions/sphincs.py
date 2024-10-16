import secrets
import time

import pyspx.shake_128f as sphf
import pyspx.shake_128s as sphs
from Crypto.PublicKey import ECC
from Crypto.Signature import eddsa


def bench_fn(fn: callable, message: bytes, sk) -> tuple[bytes, float]:
    """Sign a message and measure the time taken.

    :param fn: The signature algorithm
    :param message: The message to sign
    :param sk: The signature key
    :return: the signature value and the elapsed time
    """
    start = time.perf_counter()
    sig = fn(message, sk)
    end = time.perf_counter()
    return sig, end - start


def main():
    seed = secrets.token_bytes(sphf.crypto_sign_SEEDBYTES)
    message = "It's dangerous to go alone! Take this. 🗡️".encode()

    pk, sk = sphf.generate_keypair(seed)
    sig, elapsed = bench_fn(sphf.sign, message, sk)
    print(f"Signing with SPHINCS-128f took: {elapsed:.2}s")
    print(f"SPHINCS-128f signature size: {len(sig)} bytes")
    assert sphf.verify(message, sig, pk)

    print()

    pk, sk = sphs.generate_keypair(seed)
    sig, elapsed = bench_fn(sphs.sign, message, sk)
    print(f"Signing with SPHINCS-128s took: {elapsed:.2}s")
    print(f"SPHINCS-128s signature size: {len(sig)} bytes")
    assert sphs.verify(message, sig, pk)

    print()

    sk = ECC.generate(curve="Ed25519")
    pk = sk.public_key()

    signer = eddsa.new(sk, "rfc8032")
    start = time.perf_counter()
    sig = signer.sign(message)
    end = time.perf_counter()
    elapsed = end - start
    print(f"Signing with Ed25519 took: {elapsed:.2}s")
    print(f"Ed25519 signature size: {len(sig)} bytes")
    signer.verify(message, sig)


if __name__ == "__main__":
    main()
