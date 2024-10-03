import subprocess

from Crypto.PublicKey import ECC


def main():
    p384 = ECC.generate(curve="p384")

    with open("tmp-py.der", "wb") as f:
        data = p384.export_key(format="DER", use_pkcs8=False)
        f.write(data)

    try:
        subprocess.run(["openssl", "genpkey",
                        "-outform", "DER",
                        "-algorithm", "EC",
                        "-pkeyopt", "ec_paramgen_curve:P-384",
                        # "-pkeyopt", "ec_param_enc:explicit",
                        "-out", "tmp-ossl.der", "-quiet"], check=True)
    except subprocess.CalledProcessError:
        print("Failed to generate the private key with OpenSSL")
        return


if __name__ == "__main__":
    main()
