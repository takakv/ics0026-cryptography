from Crypto.PublicKey import ECC


def generate_sig():
    student_id = "studentid"

    message: bytes = ...

    sk: ECC = ...
    pk: ECC = ...

    sig: bytes = ...

    with open("message.bin", "wb") as f:
        f.write(message)

    with open("message.sig", "wb") as f:
        f.write(sig)

    with open(f"{student_id}.sk.pem", "w") as f:
        data: str = ...
        f.write(data)

    with open(f"{student_id}.pk.pem", "w") as f:
        data: str = ...
        f.write(data)


def verify_sig():
    student_id = "studentid"

    with open(f"{student_id}.pk.pem", "r") as f:
        pk: ECC = ...

    with open("message.bin", "rb") as f:
        message = f.read()

    with open("message.sig", "rb") as f:
        sig = f.read()


def main():
    generate_sig()
    verify_sig()


if __name__ == "__main__":
    main()
