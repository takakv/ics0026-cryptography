import argparse
import sys

import ldap  # python-ldap


def main(idcode: str):
    try:
        # SK LDAP catalogue for personal ID documents.
        connect = ldap.initialize("ldaps://esteid.ldap.sk.ee")
        connect.set_option(ldap.OPT_NETWORK_TIMEOUT, 2)
    except ldap.LDAPError:
        print("[-] Incorrect LDAP host")
        sys.exit(1)

    try:
        result = connect.search_s("c=EE", ldap.SCOPE_SUBTREE,
                                  f"serialNumber=PNOEE-{idcode}")
    except ldap.SERVER_DOWN:
        print("[-] Could not connect to the server. Is the LDAP URL correct?")
        sys.exit(1)

    # There should be an authentication and a signature cert.
    if len(result) != 2:
        print("[-] No active certificates found")
        sys.exit(1)

    cert_data_1 = result[0]
    cert_data_2 = result[1]

    cert_auth: bytes = cert_data_1[1]["userCertificate;binary"][0]
    cert_dsig: bytes = cert_data_2[1]["userCertificate;binary"][0]

    # The order should be consistent, but just to be sure....
    ou_index = cert_data_1[0].find("ou=")
    o_index = cert_data_1[0].find("o=")
    # There is a comma before 'o='.
    data1_ou = cert_data_1[0][ou_index + 3:o_index - 1]

    if data1_ou == "Digital Signature":
        cert_auth, cert_dsig = cert_dsig, cert_auth
    elif data1_ou != "Authentication":
        print(f"[-] Unexpected certificate type: '{data1_ou}'")
        sys.exit(1)

    with open(f"{idcode}.auth.der", "wb") as f:
        f.write(cert_auth)

    with open(f"{idcode}.dsig.der", "wb") as f:
        f.write(cert_dsig)


def ee_idcode(s: str):
    # Rudimentary validation.
    if len(s) == 11 and s.isdigit():
        return s
    raise argparse.ArgumentTypeError("EE ID codes are 11 digits long")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("idcode",
                        type=ee_idcode,
                        help="EE identity code to fetch certificates for.")
    args = parser.parse_args()
    main(args.idcode)
