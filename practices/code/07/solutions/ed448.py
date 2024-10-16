import sys

from Crypto.PublicKey import ECC
from Crypto.Signature import eddsa


def generate_sig():
    student_id = "studentid"

    message1 = b"This is a very authentic message"
    message2 = b"This is an inauthentic message"

    sk = ECC.generate(curve="Ed448")
    pk = sk.public_key()

    signer = eddsa.new(sk, "rfc8032")
    sig = signer.sign(message1)

    with open("message.bin", "wb") as f:
        f.write(message2)

    with open("message.sig", "wb") as f:
        f.write(sig)

    with open(f"{student_id}.sk.pem", "w") as f:
        data = sk.export_key(format="PEM")
        f.write(data)

    with open(f"{student_id}.pk.pem", "w") as f:
        data = pk.export_key(format="PEM")
        f.write(data)


def verify_sig():
    student_id = "studentid"

    with open(f"{student_id}.pk.pem", "r") as f:
        pk = ECC.import_key(f.read())

    with open("message.bin", "rb") as f:
        message = f.read()

    with open("message.sig", "rb") as f:
        sig = f.read()

    verifier = eddsa.new(pk, "rfc8032")
    try:
        verifier.verify(message, sig)
    except ValueError as e:
        print(e)
        sys.exit(1)


def main():
    generate_sig()
    verify_sig()


if __name__ == "__main__":
    main()
