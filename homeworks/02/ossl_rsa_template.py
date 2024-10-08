import argparse
import subprocess
import sys

FAIL_CODE = 1


def gen_sk(f_out: str, pwd: str) -> None:
    """Generate and export an RSA private key using OpenSSL.

    The private key is stored in PEM format and encrypted with AES-256 in
    CBC mode and using PKCS#8 format. The key derivation function used is
    PBKDF2-HMAC-SHA512 with 210000 iterations (OWASP 2023) and the encryption
    function is AES-256-CBC.

    :param f_out: The file to store the private key in
    :param pwd: The password to use for encrypting the private key
    :raises subprocess.CalledProcessError: Invoking OpenSSL failed
    """
    try:
        subprocess.run(["openssl", "genpkey", ...], check=True)
    except subprocess.CalledProcessError:
        print("Failed to generate the private key with OpenSSL")
        sys.exit(FAIL_CODE)


def gen_pk(f_in: str, f_out: str, pwd: str) -> None:
    """Derive an RSA public key from a private key using OpenSSL and export it.

    The public key is stored in PEM format.

    :param f_in: The file to read the private key from
    :param f_out: The file to store the public key in
    :param pwd: The password to use for decrypting the private key
    :raises subprocess.CalledProcessError: Invoking OpenSSL failed
    """
    pass


def encrypt(f_key: str, f_in: str, f_out: str) -> None:
    """Encrypt a file using OpenSSL.

    :param f_key: The public key file
    :param f_in: The file containing the data to encrypt
    :param f_out: The file to store the ciphertext in
    :raises subprocess.CalledProcessError: Invoking OpenSSL failed
    """
    pass


def decrypt(f_key: str, f_in: str, f_out: str, pwd: str) -> None:
    """Decrypt a file using OpenSSL.

    :param f_key: The private key file
    :param f_in: The file containing the ciphertext
    :param f_out: The file to store the decrypted data in
    :param pwd: The password to decrypt the private key with
    :raises subprocess.CalledProcessError: Invoking OpenSSL failed
    """
    pass


def main(args):
    match args.action:
        case "genpkey":
            gen_sk(args.outfile, args.pwd)
        case "pkey":
            gen_pk(args.infile, args.outfile, args.pwd)
        case "pkeyutl":
            enc = args.encrypt
            if enc:
                encrypt(args.inkey, args.infile, args.outfile)
            else:
                decrypt(args.inkey, args.infile, args.outfile, args.pwd)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # It is very messy to emulate CLI parameters similarly to those of OpenSSL.
    # If you find edge cases, please let me know.
    sub = parser.add_subparsers(dest="action", help="the task to perform")
    sp_genpkey = sub.add_parser("genpkey")
    sp_pkey = sub.add_parser("pkey")
    sp_pkeyutl = sub.add_parser("pkeyutl")

    for sp in [sp_genpkey, sp_pkey, sp_pkeyutl]:
        sp.add_argument("-o", "--out",
                        help="the output file name",
                        dest="outfile", required=True)

    for sp in [sp_pkey, sp_pkeyutl]:
        sp.add_argument("-i", "--in",
                        help="the input file name",
                        dest="infile", required=True)

    for sp in [sp_genpkey, sp_pkey]:
        sp.add_argument("-p", "--pass",
                        help="the private key password",
                        dest="pwd", required=True)

    sp_pkeyutl.add_argument("-k", "--inkey",
                            help="the input key", required=True)
    sp_pkeyutl.add_argument("-p", "--pass",
                            help="the private key password",
                            dest="pwd")
    sp_pkeyutl.add_argument("-e", "--encrypt",
                            help="whether to encrypt instead of decrypting",
                            action="store_true")

    parsed_args = parser.parse_args()
    if parsed_args.action == "encrypt" and not \
            parsed_args.encrypt and (parsed_args.pwd is None):
        sp_pkeyutl.error("password is required for decryption")

    main(parsed_args)
