import hashlib
import secrets

import hlextend  # https://github.com/stephenbradshaw/hlextend
from naive_auth import Authenticator


# The attacker does not have access to this.
def secret_setup():
    key = secrets.token_bytes(8)
    authenticator = Authenticator(key)

    user_nonce = secrets.token_bytes(8)
    # MAC = SHA256(key||data)
    user_mac = hashlib.sha256(key + user_nonce).hexdigest()

    print("Logging in as a valid user")
    ok, msg = authenticator.authenticate(user_nonce, user_mac)
    print(msg)

    return authenticator, user_nonce, user_mac


def main():
    authenticator, intercepted_nonce, intercepted_mac = secret_setup()

    print()
    print("Logging in with intercepted/replayed credentials")
    ok, msg = authenticator.authenticate(intercepted_nonce, intercepted_mac)
    print(msg)

    print()
    print("Logging in with forged credentials")
    forged_nonce = ...
    forged_mac = ...
    ok, msg = authenticator.authenticate(forged_nonce, forged_mac)
    print(msg)

    print()
    print("Intercepted nonce:", intercepted_nonce.hex())
    print("Forged nonce     :", forged_nonce.hex())


if __name__ == "__main__":
    main()
