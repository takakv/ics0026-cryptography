import hmac
import secrets

from Crypto.Cipher import ChaCha20_Poly1305


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

    key = secrets.token_bytes(32)
    cipher = ChaCha20_Poly1305.new(key=key)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(message.encode())

    cipher = ChaCha20_Poly1305.new(key=key, nonce=nonce)
    ct_bad = cipher.encrypt(received.encode())

    print(ciphertext.hex())
    print(ct_bad.hex())

    cipher = ChaCha20_Poly1305.new(key=key, nonce=nonce)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag).decode()
    print(plaintext)

    cipher = ChaCha20_Poly1305.new(key=key, nonce=nonce)
    pt = cipher.decrypt(ct_bad).decode()
    print(pt)

    cipher = ChaCha20_Poly1305.new(key=key, nonce=nonce)
    cipher.decrypt_and_verify(ct_bad, tag)


if __name__ == "__main__":
    main()
