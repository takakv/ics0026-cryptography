import argparse

KEYFILE = "key.txt"
PUBFILE = "decryption.txt"


def main(action: str, i_key: str, f_file: str, d_dir: str):
    with open(f_file, "rb") as f:
        plaintext = f.read()

    if action == "encrypt":
        pass

    if action == "decrypt":
        for i in range(5):
            decrypted = ...

            assert plaintext == decrypted  # adjust the type if necessary


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["encrypt", "decrypt"],
                        help="the action to perform")
    parser.add_argument("key", help="the secret key")
    parser.add_argument("file", help="the file to encrypt/verify against")
    parser.add_argument("dir", help="the directory of ciphertexts")

    args = parser.parse_args()
    main(args.action, args.key, args.file, args.dir)
