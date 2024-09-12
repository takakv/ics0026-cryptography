import argparse
import sys


def xor_bytes(a: bytes, b: bytes) -> bytes:
    # Warning! Does not check whether the lengths are the same.
    return bytes(l ^ r for (l, r) in zip(a, b))


def recover_words(xored: bytes, f_wordlist: str) -> tuple[str, str]:
    word_len = len(xored)

    with open(f_wordlist, "rb") as f:
        # Strip newlines to get the correct byte-length of each word.
        while base := f.readline().rstrip():
            # We know the length of the encrypted word.
            if len(base) != word_len:
                continue
            res = xor_bytes(xored, base)

            with open(f_wordlist, "rb") as fp:
                # Read the whole file in memory for fast search speed.
                if not (res in fp.read()):
                    continue

                return base.decode(), res.decode()

    return "", ""


def main(wordlist: str, c1: str, c2: str):
    # c1 = 0x3C8550F0E566
    # c2 = 0x2A925DF2ED74

    try:
        b1 = bytes.fromhex(c1)
        b2 = bytes.fromhex(c2)
    except ValueError:
        print("[-] Ciphertexts must be valid hexadecimal strings!")
        sys.exit(1)

    if len(b1) != len(b2):
        print("[-] Ciphertexts must have the same length!")
        sys.exit(1)

    # XOR both halves to get rid of the repeating key since
    # (a ^ k) ^ (b ^ k) = a ^ b
    xored = xor_bytes(b1, b2)

    # Brute force the words.
    print("[+] Brute forcing the words.", "This may take a while...")
    m1, m2 = recover_words(xored, wordlist)
    if m1 == m2:
        print("[-] Failed to recover the words.")
        return

    # We cannot recover the word order since we could recover two
    # separate keys that both give a different word order.
    print(f"[+] Found ‘{m1}’, ‘{m2}’ as candidates")
    print(f"[+] The plaintext is: ‘{m1}{m2}’ or ‘{m2}{m1}’")


if __name__ == "__main__":
    # Example wordlist: https://www.mit.edu/~ecprice/wordlist.10000
    parser = argparse.ArgumentParser()
    parser.add_argument("wordlist", help="Dictionary file — one word per line")
    parser.add_argument("ct_1", help="First ciphertext word as a HEX string")
    parser.add_argument("ct_2", help="Second ciphertext word as a HEX string")
    args = parser.parse_args()

    main(args.wordlist, args.ct_1, args.ct_2)
