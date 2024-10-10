import hmac
import secrets


# noinspection SpellCheckingInspection
def main():
    message = "MACs are important!"
    key = secrets.token_bytes(16)
    mac = hmac.digest(key, message.encode(), "sha256")

    received = "MACs are importantǃ"
    check_mac = hmac.digest(key, received.encode(), "sha256")

    # Verify using constant-time comparison!
    print(hmac.compare_digest(mac, check_mac))
    print(hmac.compare_digest(mac, hmac.digest(key, message.encode(),
                                               "sha256")))

    # TODO: encrypt the original message using authenticated chacha20
    ciphertext, tag = ...

    # TODO: encrypt the received message using authenticated chacha20 using the same key and nonce
    ct_bad = ...

    print(ciphertext.hex())
    print(ct_bad.hex())

    # TODO: decrypt and authenticate the original message with the original tag
    ...

    # TODO: decrypt and authenticate the received message with the original tag
    ...


if __name__ == "__main__":
    main()
