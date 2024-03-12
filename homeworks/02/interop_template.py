import argparse
import subprocess
import sys

from Crypto.PublicKey import RSA

FAIL_CODE = 1


def read_sk(f_sk: str, pwd: str) -> RSA.RsaKey:
    """Read a password protected RSA private key from a file.

    :param f_sk: The file to read the private key from
    :param pwd: The password to decrypt the private key
    :return: an RSA key object
    """
    pass


def read_pk(f_pk: str) -> RSA.RsaKey:
    """Read an RSA public key from a file.

    :param f_pk: The file to read the public key from
    :return: an RSA key object
    """
    pass


def gen_priv_openssl(f_out: str, pwd: str) -> None:
    """Generate and export an RSA private key using OpenSSL.

    The private key is stored in PEM format and encrypted with AES-256 in
    CBC mode and using PKCS#8 format.

    :param f_out: The file to store the private key in
    :param pwd: The password to use for encrypting the private key
    :raises subprocess.CalledProcessError: Invoking OpenSSL failed
    """
    try:
        pass
    except subprocess.CalledProcessError:
        print("Failed to generate the private key with OpenSSL")
        sys.exit(FAIL_CODE)


def gen_pub_openssl(f_in: str, f_out: str, pwd: str) -> None:
    """Derive an RSA public key from a private key using OpenSSL and export it.

    The public key is stored in PEM format.

    :param f_in: The file to read the private key from
    :param f_out: The file to store the public key in
    :param pwd: The password to use for decrypting the private key
    :raises subprocess.CalledProcessError: Invoking OpenSSL failed
    """
    pass


def gen_priv_py(f_out: str, pwd: str) -> None:
    """Generate and export an RSA private key.

    The private key is stored in PEM format and encrypted with AES-256 in
    CBC mode and using PKCS#8 format.

    :param f_out: The filename to store the private key in
    :param pwd: The password to use for encrypting the private key
    """
    pass


def gen_pub_py(f_in: str, f_out: str, pwd: str) -> None:
    """Derive an RSA public key from a private key and export it.

    The public key is stored in PEM format.

    :param f_in: The file to read the private key from
    :param f_out: The file to store the public key in
    :param pwd: The password to use for decrypting the private key
    """
    pass


def encrypt_openssl(f_key: str, f_in: str, f_out: str) -> None:
    """Encrypt a file using OpenSSL.

    :param f_key: The public key file
    :param f_in: The file containing the data to encrypt
    :param f_out: The file to store the ciphertext in
    :raises subprocess.CalledProcessError: Invoking OpenSSL failed
    """
    pass


def decrypt_openssl(f_key: str, f_in: str, f_out: str, pwd: str) -> None:
    """Decrypt a file using OpenSSL.

    :param f_key: The private key file
    :param f_in: The file containing the ciphertext
    :param f_out: The file to store the decrypted data in
    :param pwd: The password to decrypt the private key with
    :raises subprocess.CalledProcessError: Invoking OpenSSL failed
    """
    pass


def encrypt_py(f_key: str, f_in: str, f_out: str) -> None:
    """Encrypt a file.

    :param f_key: The public key file
    :param f_in: The file containing the data to encrypt
    :param f_out: The file to store the ciphertext in
    :raises subprocess.CalledProcessError: Invoking OpenSSL failed
    """
    pass


def decrypt_py(f_key: str, f_in: str, f_out: str, pwd: str) -> None:
    """Decrypt a file.

    :param f_key: The private key file
    :param f_in: The file containing the ciphertext
    :param f_out: The file to store the decrypted data in
    :param pwd: The password to decrypt the private key with
    """
    pass


def main(args):
    use_ossl = args.openssl

    match args.action:
        case "genpkey":
            if use_ossl:
                gen_priv_openssl(args.outfile, args.pwd)
            else:
                gen_priv_py(args.outfile, args.pwd)
        case "pkey":
            if use_ossl:
                gen_pub_openssl(args.infile, args.outfile, args.pwd)
            else:
                gen_pub_py(args.infile, args.outfile, args.pwd)
        case "pkeyutl":
            encrypt = args.encrypt

            if use_ossl:
                if encrypt:
                    encrypt_openssl(args.inkey, args.infile, args.outfile)
                else:
                    decrypt_openssl(args.inkey, args.infile, args.outfile,
                                    args.pwd)
            else:
                if encrypt:
                    encrypt_py(args.inkey, args.infile, args.outfile)
                else:
                    decrypt_py(args.inkey, args.infile, args.outfile, args.pwd)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # It is very messy to emulate CLI parameters similarly to those of OpenSSL.
    sub = parser.add_subparsers(dest="action", help="the task to perform")
    sp_genpkey = sub.add_parser("genpkey")
    sp_pkey = sub.add_parser("pkey")
    sp_pkeyutl = sub.add_parser("pkeyutl")

    for sp in [sp_genpkey, sp_pkey, sp_pkeyutl]:
        sp.add_argument("-x", "--openssl",
                        help="whether to use OpenSSL for the action",
                        action="store_true")
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
