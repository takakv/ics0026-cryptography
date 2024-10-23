import argparse
import os
import sys

import ldap  # python-ldap

skos = {
    "Identity card of Estonian citizen": "",
    "Identity card of European Union citizen": "",  # no conflict with EE ID card
    "Diplomatic identity card": "diplomatic-id",
    "Residence card of long-term resident": "",  # no conflict
    "Residence card of temporary residence citizen": "",  # no conflict
    "Digital identity card": "digi-id",
    "Digital identity card of e-resident": "",  # no conflict
    "Mobile-ID": "m-id"
}


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
    if len(result) < 2:
        print("[-] No active certificates found")
        sys.exit(1)

    if not os.path.isdir(f"{idcode}"):
        os.mkdir(f"{idcode}")

    for data in result:
        meta = data[0]
        ou_index = meta.find("ou=")
        o_index = meta.find("o=")
        dc_index = meta.find("dc=")
        # There is a comma before 'o='.
        ou = meta[ou_index + 3:o_index - 1]
        # There is a comma before 'dc='.
        o = meta[o_index + 2:dc_index - 1]

        try:
            ctype = skos[o]
        except KeyError:
            print(f"[-] Unknown certificate type: '{o}'")
            sys.exit(1)

        # Add the dot suffix only if the type goes into the filename.
        if ctype:
            ctype = f".{ctype}"

        match ou:
            case "Authentication":
                purpose = "auth"
            case "Digital Signature":
                purpose = "dsig"
            case _:
                print(f"[-] Unknown certificate purpose: '{ou}'")
                sys.exit(1)

        cert = data[1]["userCertificate;binary"][0]
        with open(f"{idcode}/{idcode}{ctype}.{purpose}.der", "wb") as f:
            f.write(cert)


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
