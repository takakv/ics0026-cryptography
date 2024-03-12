import subprocess

PREFIX = ["python3", "interop.py"]
PASS = ["--pass", "secret"]
OSSL = ["--openssl"]


def gen_priv(f_out: str, ossl: bool) -> None:
    ossl = OSSL if ossl else []

    subprocess.run(PREFIX + ["genpkey"] + ossl +
                   ["--out", f_out] + PASS,
                   check=True)


def gen_pub(f_in: str, f_out: str, ossl: bool) -> None:
    ossl = OSSL if ossl else []

    subprocess.run(PREFIX + ["pkey"] + ossl +
                   ["--in", f_in, "--out", f_out] + PASS,
                   check=True)


def enc(f_key: str, f_in: str, f_out: str, ossl: bool) -> None:
    ossl = OSSL if ossl else []

    subprocess.run(
        PREFIX + ["pkeyutl"] + ossl +
        ["--inkey", f_key, "--in", f_in, "--out", f_out, "--encrypt"],
        check=True)


def dec(f_key: str, f_in: str, f_out: str, ossl: bool) -> None:
    ossl = OSSL if ossl else []

    subprocess.run(
        PREFIX + ["pkeyutl"] + ossl +
        ["--inkey", f_key, "--in", f_in, "--out", f_out] + PASS,
        check=True)


def is_openssl(b: bool) -> str:
    return "OpenSSL" if b else "py"


def test():
    message = "It's dangerous to go alone! Take this. 🗡️".encode("UTF-8")
    f_msg = "message.txt"

    with open(f_msg, "wb") as f:
        f.write(message)

    options = [True, False]

    for b1 in options:
        f_sk = "key.pem"
        gen_priv(f_sk, b1)

        for b2 in options:
            f_pk = "pub.pem"
            gen_pub(f_sk, f_pk, b2)

            for b3 in options:
                f_enc = "data.enc"
                enc(f_pk, f_msg, f_enc, b3)

                for b4 in options:
                    f_dec = "data.dec"
                    dec(f_sk, f_enc, f_dec, b4)

                    with open(f_dec, "rb") as f:
                        decrypted = f.read()

                    if decrypted != message:
                        print("Operation failed with:")
                        print("\tsk:", is_openssl(b1))
                        print("\tpk:", is_openssl(b2))
                        print("\tct:", is_openssl(b3))
                        print("\tpt:", is_openssl(b4))


if __name__ == "__main__":
    test()
