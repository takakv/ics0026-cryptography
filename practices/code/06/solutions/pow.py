import datetime
import hashlib


def l0_bits(bs: bytes) -> int:
    """Return the number of leading 0 bits.

    :param bs: the byte string
    :return: the number of leading 0 bits
    """
    n = 0
    for b in bs:
        for _ in range(8):
            # Not a leading 0 bit
            if b & 0x80 != 0:
                return n
            # Set the first bit to 0 so that we can shift
            b &= 0x7F
            b <<= 1
            n += 1

    # Everything must be 0
    return len(bs) * 8


def bruteforce(seed: bytes, difficulty: int = 0) -> tuple[int, bytes]:
    """Find a nonce such that the hash starts with >= x 0-bits.

    :param seed: the seed of the hash function
    :param difficulty: the minimum number of expected 0-bits
    :return: the suitable nonce and the corresponding SHA256 input
    """
    assert difficulty >= 0

    nonce = 0
    lead = 0

    if difficulty == 0:
        ip = seed + nonce.to_bytes(8, "big")
        res = hashlib.sha256(hashlib.sha256(ip).digest()).digest()
        nonce += 1
    else:
        while lead < difficulty:
            ip = seed + nonce.to_bytes(8, "big")
            res = hashlib.sha256(hashlib.sha256(ip).digest()).digest()
            lead = l0_bits(res)
            nonce += 1

    # Ignore the last addition for the correct count.
    nonce -= 1
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
