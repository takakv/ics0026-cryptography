import secrets
import time

import pyspx.shake_128s as sphs


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
    seed = secrets.token_bytes(...)
    message = "It's dangerous to go alone! Take this. 🗡️".encode()

    pk, sk = ...
    sig, elapsed = bench_fn(..., message, sk)
    print(f"Signing with SPHINCS-128f took: {elapsed:.2}s")
    print(f"SPHINCS-128f signature size: {len(sig)} bytes")
    assert ...

    print()

    pk, sk = ...
    sig, elapsed = bench_fn(..., message, sk)
    print(f"Signing with SPHINCS-128s took: {elapsed:.2}s")
    print(f"SPHINCS-128s signature size: {len(sig)} bytes")
    assert sphs.verify(message, sig, pk)

    print()

    sk = ...
    pk = ...

    start = time.perf_counter()
    sig = ...
    end = time.perf_counter()
    elapsed = end - start
    print(f"Signing with Ed25519 took: {elapsed:.2}s")
    print(f"Ed25519 signature size: {len(sig)} bytes")
    assert ...


if __name__ == "__main__":
    main()
