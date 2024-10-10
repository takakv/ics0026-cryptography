import base64
import hashlib
import secrets
import time

from argon2 import PasswordHasher  # https://github.com/hynek/argon2-cffi

SALT_LEN = 16


def hash_sha256(passwords: list[bytes], filename: str):
    with open(filename, "w") as f:
        for pwd in passwords:
            digest = hashlib.sha256(pwd).hexdigest()
            f.write(f"{digest}\n")


def hash_salted_sha256(passwords: list[bytes], filename: str):
    with open(filename, "w") as f:
        for pwd in passwords:
            salt = secrets.token_urlsafe(SALT_LEN)
            digest = hashlib.sha256(pwd + salt.encode()).hexdigest()
            f.write(f"{digest}:{salt}\n")


def hash_scrypt(passwords: list[bytes], filename: str):
    # OWASP recommendations for scrypt.
    n = 2 ** 17  # iteration count
    r = 8  # block size
    p = 1  # parallelism factor

    # Needed for hashlib's OpenSSL scrypt delegation to work.
    ossl_maxmem = 2 ** 28

    with open(filename, "w") as f:
        for pwd in passwords:
            salt = secrets.token_bytes(SALT_LEN)
            digest = hashlib.scrypt(pwd, salt=salt, dklen=32,
                                    n=n, r=r, p=p,
                                    maxmem=ossl_maxmem)

            b64_salt = base64.b64encode(salt).decode()
            b64_digest = base64.b64encode(digest).decode()
            f.write(f"SCRYPT:{n}:{r}:{p}:{b64_salt}:{b64_digest}\n")


def hash_pbkdf2_hmac_sha256(passwords: list[bytes], filename: str):
    # OWASP recommendation for PBKDF2.
    iterations = 600_000
    with open(filename, "w") as f:
        for pwd in passwords:
            salt = secrets.token_bytes(SALT_LEN)
            digest = hashlib.pbkdf2_hmac("sha256", pwd, salt,
                                         iterations, dklen=32)
            b64_salt = base64.b64encode(salt).decode()
            b64_digest = base64.b64encode(digest).decode()
            f.write(f"sha256:{iterations}:{b64_salt}:{b64_digest}\n")


def hash_argon2id(passwords: list[bytes], filename: str):
    # argon2-cffi's defaults are already stronger than the OWASP
    # recommendations. Use 1 for the parallelism for a fairer comparison
    # with the other methods.
    ph = PasswordHasher(parallelism=1)
    with open(filename, "w") as f:
        for pwd in passwords:
            salt = secrets.token_bytes(SALT_LEN)
            digest = ph.hash(pwd, salt=salt)
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

    passwords = passwords[:100]

    measure_performance(hash_pbkdf2_hmac_sha256, "PBKDF2-HMAC-SHA256",
                        passwords, "pbkdf2.txt")
    measure_performance(hash_scrypt, "scrypt",
                        passwords, "scrypt.txt")
    measure_performance(hash_argon2id, "argon2id",
                        passwords, "argon2id.txt")


if __name__ == "__main__":
    main()
