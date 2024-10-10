import base64
import hashlib
import secrets
import time

from argon2 import PasswordHasher  # https://github.com/hynek/argon2-cffi

SALT_LEN = 16


def hash_sha256(passwords: list[bytes], filename: str):
    with open(filename, "w") as f:
        for pwd in passwords:
            digest = ...
            f.write(f"{digest}\n")


def hash_salted_sha256(passwords: list[bytes], filename: str):
    with open(filename, "w") as f:
        for pwd in passwords:
            salt = ...
            digest = ...
            f.write(f"{digest}:{salt}\n")


def hash_scrypt(passwords: list[bytes], filename: str):
    # OWASP recommendations for scrypt.
    n = ...  # iteration count
    r = ... # block size
    p = ...  # parallelism factor

    # Needed for hashlib's OpenSSL scrypt delegation to work.
    ossl_maxmem = 2 ** 28

    with open(filename, "w") as f:
        for pwd in passwords:
            salt = ...
            digest = ...

            b64_salt = base64.b64encode(salt).decode()
            b64_digest = base64.b64encode(digest).decode()
            f.write(f"SCRYPT:{n}:{r}:{p}:{b64_salt}:{b64_digest}\n")


def hash_pbkdf2_hmac_sha256(passwords: list[bytes], filename: str):
    # OWASP recommendation for PBKDF2.
    iterations = ...
    with open(filename, "w") as f:
        for pwd in passwords:
            salt = ...
            digest = ...

            b64_salt = base64.b64encode(salt).decode()
            b64_digest = base64.b64encode(digest).decode()
            f.write(f"sha256:{iterations}:{b64_salt}:{b64_digest}\n")


def hash_argon2id(passwords: list[bytes], filename: str):
    # argon2-cffi's defaults are already stronger than the OWASP
    # recommendations. Use 1 for the parallelism for a fairer comparison
    # with the other methods.
    ph = ...
    with open(filename, "w") as f:
        for pwd in passwords:
            salt = ...
            digest = ...
            f.write(f"{digest}\n")


def measure_performance(fn: callable, name: str,
                        passwords: list[bytes], filename: str):
    start_time = time.perf_counter()
    fn(passwords, filename)
    elapsed = time.perf_counter() - start_time
    print(f"Took: {elapsed}s for {len(passwords)}"
          f" passwords ({name})")


def main():
    # Read all passwords into memory for discrete iterations.
    passwords: list[bytes] = []
    # https://raw.githubusercontent.com/danielmiessler/SecLists/refs/heads/master/Passwords/Common-Credentials/10k-most-common.txt
    with open("10k-most-common.txt", "rb") as f:
        for p in f.readlines():
            passwords.append(p[:-1])

    measure_performance(hash_sha256, "SHA2-256",
                        passwords, "sha256.txt")
    measure_performance(hash_salted_sha256, "salted SHA2-256",
                        passwords, "sha256.salted.txt")

    # Cut down the number of passwords for efficiency.
    passwords = passwords[:100]

    measure_performance(hash_pbkdf2_hmac_sha256, "PBKDF2-HMAC-SHA256",
                        passwords, "pbkdf2.txt")
    measure_performance(hash_scrypt, "scrypt",
                        passwords, "scrypt.txt")
    measure_performance(hash_argon2id, "argon2id",
                        passwords, "argon2id.txt")


if __name__ == "__main__":
    main()
