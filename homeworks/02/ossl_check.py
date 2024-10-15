import subprocess
import sys

import pyasn1.error
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.IO import PEM
from Crypto.PublicKey import RSA
from pyasn1.codec.der import decoder
from pyasn1_modules.rfc5208 import EncryptedPrivateKeyInfo
from pyasn1_modules.rfc8018 import id_PBES2, id_PBKDF2, id_hmacWithSHA512, \
    PBES2_params, PBKDF2_params, aes256_CBC_PAD

PREFIX = ["python3", "ossl_rsa.py"]
PASS = ["--pass", "secret"]

ITER_COUNT = 210000
HASH_ALGO = SHA256


def check_pem(filename: str) -> None:
    """Test whether a file is in PEM format.

    Aborts the program execution if that is not the case.

    :param filename: The name of the file to check
    """
    with open(filename, "r") as f:
        data = f.read()

    try:
        PEM.decode(data)
    except ValueError:
        print(f"File {filename} is not in PEM format")
        sys.exit(1)


def validate_sk_enc(f_sk: str) -> None:
    """Test whether the private key has been correct encrypted.

    :param f_sk: The private key file
    """
    with open(f_sk, "r") as f:
        data = f.read()
    sk_der, pem_header, _ = PEM.decode(data)

    if pem_header != "ENCRYPTED PRIVATE KEY":
        print("[-] Incorrect private key format")
        return

    sk_asn1, _ = decoder.decode(sk_der, asn1Spec=EncryptedPrivateKeyInfo())
    algorithm_identifier = sk_asn1.getComponentByName("encryptionAlgorithm")
    algorithm_oid = algorithm_identifier.getComponentByName("algorithm")

    # Verify that the private key is in the correct encrypted format.
    if algorithm_oid != id_PBES2:
        print("[-] Wrong key encryption format")
        return

    # Verify that the private key was encrypted with the correct parameters.
    pbes2_params, _ = decoder.decode(
        algorithm_identifier.getComponentByName("parameters"),
        asn1Spec=PBES2_params())
    kdf = pbes2_params.getComponentByName("keyDerivationFunc")
    enc_scheme = pbes2_params.getComponentByName("encryptionScheme")

    # KDF must be PBKDF2.
    kdf_oid = kdf.getComponentByName("algorithm")
    if kdf_oid != id_PBKDF2:
        print("[-] Wrong key derivation algorithm for private key password")
        return

    # Fetch the PBKDF2 parameters.
    pbkdf2_params, _ = decoder.decode(kdf.getComponentByName("parameters"),
                                      asn1Spec=PBKDF2_params())

    # PBKDF2 PRF must be HMAC-SHA512.
    prf = pbkdf2_params.getComponentByName("prf")
    prf_oid = prf.getComponentByName("algorithm")
    if prf_oid != id_hmacWithSHA512:
        print("[-] Wrong PRF algorithm for te private key PBKDF2")
        return

    # PBKDF2 iteration count must be as specified.
    iter_count = pbkdf2_params.getComponentByName("iterationCount")
    if iter_count != ITER_COUNT:
        print("[-] Wrong PBKDF2 iteration count for encrypted private key:", iter_count)
        return

    # Private key must be encrypted with AES-256-CBC.
    enc_algorithm = enc_scheme.getComponentByName("algorithm")
    if enc_algorithm != aes256_CBC_PAD:
        print("[-] Wrong encryption algorithm for encrypted private key")


def read_sk(f_sk: str, pwd: str) -> RSA.RsaKey:
    """Read a password protected RSA private key from a file.

    :param f_sk: The file to read the private key from
    :param pwd: The password to decrypt the private key
    :return: an RSA key object
    """
    with open(f_sk, "rb") as f:
        key = RSA.import_key(f.read(), pwd)
    return key


def read_pk(f_pk: str) -> RSA.RsaKey:
    """Read an RSA public key from a file.

    :param f_pk: The file to read the public key from
    :return: an RSA key object
    """
    with open(f_pk, "rb") as f:
        key = RSA.import_key(f.read())
    return key


def gen_sk_check(f_out: str) -> None:
    """Generate and export an RSA private key.

    The private key is stored in PEM format and encrypted with AES-256 in
    CBC mode and using PKCS#8 format.

    :param f_out: The filename to store the private key in
    """
    key = RSA.generate(3072)
    with open(f_out, "wb") as f:
        f.write(key.export_key(passphrase=PASS[1], pkcs=8,
                               format="PEM",
                               protection="PBKDF2WithHMAC-SHA512AndAES256-CBC",
                               prot_params={"iteration_count": ITER_COUNT}))


def gen_pk_check(f_in: str, f_out: str) -> None:
    """Derive an RSA public key from a private key and export it.

    The public key is stored in PEM format.

    :param f_in: The file to read the private key from
    :param f_out: The file to store the public key in
    """
    key = read_sk(f_in, PASS[1])

    with open(f_out, "wb") as f:
        f.write(key.public_key().export_key(format="PEM"))


def enc_check(f_key: str, f_in: str, f_out: str) -> None:
    """Encrypt a file using RSA OAEP.

    :param f_key: The public key file
    :param f_in: The file containing the data to encrypt
    :param f_out: The file to store the ciphertext in
    """
    key = read_pk(f_key)
    cipher = PKCS1_OAEP.new(key, hashAlgo=HASH_ALGO)

    with open(f_in, "rb") as f:
        pt = f.read()

    ct = cipher.encrypt(pt)

    with open(f_out, "wb") as f:
        f.write(ct)


def dec_check(f_key: str, f_in: str, f_out: str) -> None:
    """Decrypt a file encrypted with RSA OAEP.

    :param f_key: The private key file
    :param f_in: The file containing the ciphertext
    :param f_out: The file to store the decrypted data in
    """
    key = read_sk(f_key, PASS[1])
    cipher = PKCS1_OAEP.new(key, hashAlgo=HASH_ALGO)

    with open(f_in, "rb") as f:
        ct = f.read()

    pt = cipher.decrypt(ct)

    with open(f_out, "wb") as f:
        f.write(pt)


def gen_sk(f_out: str, ossl: bool) -> None:
    if not ossl:
        gen_sk_check(f_out)
        return

    subprocess.run(PREFIX + ["genpkey", "--out", f_out] + PASS,
                   check=True)


def gen_pk(f_in: str, f_out: str, ossl: bool) -> None:
    if not ossl:
        gen_pk_check(f_in, f_out)
        return

    subprocess.run(PREFIX + ["pkey", "--in", f_in, "--out", f_out] + PASS,
                   check=True)


def enc(f_key: str, f_in: str, f_out: str, ossl: bool) -> None:
    if not ossl:
        enc_check(f_key, f_in, f_out)
        return

    subprocess.run(
        PREFIX + ["pkeyutl", "--inkey", f_key, "--in", f_in, "--out", f_out, "--encrypt"],
        check=True)


def dec(f_key: str, f_in: str, f_out: str, ossl: bool) -> None:
    if not ossl:
        dec_check(f_key, f_in, f_out)

    subprocess.run(
        PREFIX + ["pkeyutl", "--inkey", f_key, "--in", f_in, "--out", f_out] + PASS,
        check=True)


def is_openssl(b: bool) -> str:
    return "OpenSSL" if b else "py"


def test():
    message = "It's dangerous to go alone! Take this. 🗡️".encode("UTF-8")
    f_msg = "message.txt"

    with open(f_msg, "wb") as f:
        f.write(message)

    options = [True, False]
    failed = False

    try:
        for b1 in options:
            f_sk = "key.pem"
            gen_sk(f_sk, b1)
            check_pem(f_sk)

            if b1:
                try:
                    validate_sk_enc(f_sk)
                except pyasn1.error.PyAsn1Error:
                    print("⚠️ The private key is not in the expected format")
                    sys.exit(1)

            for b2 in options:
                f_pk = "pub.pem"
                gen_pk(f_sk, f_pk, b2)
                check_pem(f_pk)

                for b3 in options:
                    f_enc = "data.enc"
                    enc(f_pk, f_msg, f_enc, b3)

                    for b4 in options:
                        f_dec = "data.dec"
                        dec(f_sk, f_enc, f_dec, b4)

                        with open(f_dec, "rb") as f:
                            decrypted = f.read()

                        if decrypted != message:
                            failed = True
                            print(f"Chain failed with:")
                            print("\tsk:", is_openssl(b1))
                            print("\tpk:", is_openssl(b2))
                            print("\tct:", is_openssl(b3))
                            print("\tpt:", is_openssl(b4))
    except subprocess.CalledProcessError:
        print("⚠️ Implementation error likely")
        sys.exit(1)

    if not failed:
        print("✅ The implementation seems functional")
        return

    sys.exit(1)


if __name__ == "__main__":
    test()
