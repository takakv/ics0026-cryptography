import signal  # needed to kill the naive modexp after some time
import time

import gmpy2


def bench_modexp(fn: callable, base: int, exp: int, mod: int,
                 n_iter: int = 10) -> float:
    """Benchmark n iterations of the modular exponentiation.

    :param fn: The modular exponentiation function
    :param base: The base
    :param exp: The exponent
    :param mod: The modulus
    :param n_iter: The number of calls
    :return: the elapsed time
    """
    start = time.perf_counter()
    for _ in range(n_iter):
        fn(base, exp, mod)
    end = time.perf_counter()
    return end - start


def print_fn_bench(fn: callable, elapsed: float) -> None:
    """Pretty-print the benchmark result.

    :param fn: The function that was benchmarked
    :param elapsed: The elapsed time
    """
    print(f"Took: {elapsed:.2}s for '{fn.__name__}'")


def naive_modexp(base: int, exp: int, mod: int) -> int:
    """Perform naive modular exponentiation.

    :param base: The base
    :param exp: The exponent
    :param mod: The modulus
    :return: The modular exponentiation result
    """
    # TODO: implement naive exponentiation.
    return 0


def handle_timeout(_, __):
    raise RuntimeError


def main():
    # TODO: ‘cryptographically’ generate 3 3072-bit integers.
    nums = [...]
    # TODO: Sort the numbers such that a < b < c.

    # It is very unlikely that any two numbers are equal.
    assert nums[0] < nums[1] < nums[2]

    base = nums[0]
    exp = nums[1]
    mod = nums[2]

    # TODO: ensure that gmpy2.powmod_sec() gets an odd modulus.

    pow_fns = [pow, gmpy2.powmod, gmpy2.powmod_sec]
    for fn in pow_fns:
        elapsed = bench_modexp(fn, base, exp, mod)
        print_fn_bench(fn, elapsed)

    abort_after = 5  # seconds to abort after

    signal.signal(signal.SIGALRM, handle_timeout)
    signal.alarm(abort_after)
    try:
        naive_modexp(base, exp, mod)
    except RuntimeError:
        print(f"Stopped '{naive_modexp.__name__}' after {abort_after}s")


if __name__ == "__main__":
    main()
