import secrets
import time

from gmpy2 import gmpy2


def is_prime(p: int, n_iter: int = 64) -> bool:
    """Determine whether a number is probably prime.

    :param p: The number to test for primality
    :param n_iter: The number of algorithm iterations
    :return: true if the number is probably prime
    """
    return gmpy2.is_prime(p, n_iter)


def bench_fn(fn: callable, bitcount: int) -> tuple[int, float]:
    """Find a prime of the desired length and measure the time taken.

    :param fn: The prime-finding function
    :param bitcount: The desired prime bit-length
    :return: the generated prime and the elapsed time
    """
    start = time.perf_counter()
    res = fn(bitcount)
    end = time.perf_counter()
    return res, end - start


def find_random_prime(bitcount: int) -> int:
    """Find an n-bit prime using random search.

    :param bitcount: The desired prime bit-length
    :return: the n-bit prime
    """
    n = 0
    while not is_prime(n) or n.bit_length() != bitcount:
        n = secrets.randbits(bitcount)
    return n


def find_incremental_prime(bitcount: int) -> int:
    """Find an n-bit prime using incremental search.

    :param bitcount: The desired prime bit-length
    :return: the n-bit prime
    """
    n = 0
    while n.bit_length() != bitcount:
        n = secrets.randbits(bitcount)

    # n could be even
    if gmpy2.is_even(n):
        n += 1

    while not is_prime(n):
        n += 2

    # It could be that the next prime is larger than n-bits,
    # although this is quite unlikely.
    if n.bit_length() > bitcount:
        n = find_incremental_prime(bitcount)

    return n


def find_prime_lib(bitcount: int) -> int:
    """Find an n-bit prime using library functions.

    :param bitcount: The desired prime bit-length
    :return: the n-bit prime
    """
    n = 0
    while n.bit_length() != bitcount:
        n = secrets.randbits(bitcount)
    n = gmpy2.next_prime(n)

    # It could be that the next prime is larger than n-bits,
    # although this is quite unlikely.
    if n.bit_length() > bitcount:
        n = find_prime_lib(bitcount)

    return n


def check_primes_and_print(p: int, q: int,
                           bp: float, bq: float,
                           req_bits: int, method: str) -> None:
    """Verify required primality and print the benchmark.

    :param p: The first prime
    :param q: The second prime
    :param bp: The time taken to generate p
    :param bq: The time taken to generate q
    :param req_bits: The required prime bit-length
    :param method: The method used to obtain the primes
    """
    assert p.bit_length() == req_bits and is_prime(p)
    assert q.bit_length() == req_bits and is_prime(q)

    elapsed = (bp + bq) / 2
    print(f"Finding primes ({method}) took: {elapsed:.2}s")


def main():
    required_bits = 1536
    p, p_elapsed = bench_fn(find_random_prime, required_bits)
    q, q_elapsed = bench_fn(find_random_prime, required_bits)

    check_primes_and_print(p, q, p_elapsed, q_elapsed, required_bits, "random")

    p2, p2_elapsed = bench_fn(find_incremental_prime, required_bits)
    q2, q2_elapsed = bench_fn(find_incremental_prime, required_bits)

    check_primes_and_print(p2, q2, p2_elapsed, q2_elapsed, required_bits, "incremental")

    p3, p3_elapsed = bench_fn(find_incremental_prime, required_bits)
    q3, q3_elapsed = bench_fn(find_prime_lib, required_bits)

    check_primes_and_print(p3, q3, p3_elapsed, q3_elapsed, required_bits, "lib")

    print()

    print("Semiprime bits (1):", (p * q).bit_length())
    print("Semiprime bits (2):", (p2 * q2).bit_length())
    print("Semiprime bits (3):", (p3 * q3).bit_length())


if __name__ == "__main__":
    main()
