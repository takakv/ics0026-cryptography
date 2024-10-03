import subprocess


def main():
    # TODO: generate private key
    p384 = ...

    with open("tmp-py.der", "wb") as f:
        # TODO: export private key
        pass

    try:
        # TODO: provide proper OpenSSL parameters
        subprocess.run(["openssl", "-out", "tmp-ossl.der", "-quiet"], check=True)
    except subprocess.CalledProcessError:
        print("Failed to generate the private key with OpenSSL")
        return


if __name__ == "__main__":
    main()
