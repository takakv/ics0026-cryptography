import datetime


def l0_bits(bs: bytes) -> int:
    """Return the number of leading 0 bits.

    :param bs: the byte string
    :return: the number of leading 0 bits
    """
    pass


def bruteforce(seed: bytes, difficulty: int = 0) -> tuple[int, bytes]:
    """Find a nonce such that the hash starts with >= x 0-bits.

    :param seed: the seed of the hash function
    :param difficulty: the minimum number of expected 0-bits
    :return: the suitable nonce and the corresponding SHA256 input
    """
    assert difficulty >= 0

    nonce = 0
    res = b""

    ...

    return nonce, res


def main():
    difficulty = 25
    seed = b"ICS0026"

    start = datetime.datetime.now()
    nonce, res = bruteforce(seed, difficulty)
    end = datetime.datetime.now()

    ip = seed + nonce.to_bytes(8, "big")

    elapsed = (end - start).total_seconds()
    unit_time = round(nonce / (elapsed * 1_000_000), 4)

    print(f"Solved in {elapsed} sec ({unit_time} Mhash/sec)")
    print("Input:", ip.hex())
    print("Solution:", res.hex())
    print("Nonce:", nonce)


if __name__ == "__main__":
    main()
