import sys

# Package 'pyscard'
from smartcard.CardConnection import CardConnection
from smartcard.CardRequest import CardRequest
from smartcard.CardType import AnyCardType
from smartcard.util import toHexString


class CC:
    def __init__(self):
        # Wait until a card is inserted into any reader.
        self.channel = CardRequest(timeout=100, cardType=AnyCardType()).waitforcard().connection
        print("Selected reader:", self.channel.getReader())

        # Use T=0 for compatibility and simplicity.
        try:
            self.channel.connect(CardConnection.T0_protocol)
        except:
            # Fallback to T=1 if the reader does not support T=0.
            self.channel.connect(CardConnection.T1_protocol)

        self._detect()

    def _detect(self):
        atr = self.channel.getATR()
        if atr == [0x3B, 0xDB, 0x96, 0x00, 0x80, 0xB1, 0xFE, 0x45, 0x1F, 0x83, 0x00,
                   0x12, 0x23, 0x3F, 0x53, 0x65, 0x49, 0x44, 0x0F, 0x90, 0x00, 0xF1]:
            print("Estonian ID card")
        else:
            print("Unknown card:", toHexString(atr))
            sys.exit(1)

    def send(self, apdu: list[int]):
        data, sw1, sw2 = self.channel.transmit(apdu)

        # Success.
        if [sw1, sw2] == [0x90, 0x00]:
            return data
        # Signals that there is more data to read.
        elif sw1 == 0x61:
            return self.send([0x00, 0xC0, 0x00, 0x00, sw2])  # GET RESPONSE of sw2 bytes
        elif sw1 == 0x6C:
            return self.send(apdu[0:4] + [sw2])  # resend APDU with Le = sw2
        elif sw1 == 0x63 and len(data) == 0:
            # PIN tries counter.
            return sw2
        # Probably an error condition.
        else:
            print("Error: %02x %02x, sending APDU: %s" % (sw1, sw2, toHexString(apdu)))
            sys.exit(1)


def main():
    cc = CC()

    cmd_select = [0x00, 0xA4, 0x04, 0x00]
    aid = [0xa0, 0x00, 0x00, 0x00, 0x77, 0x01, 0x08, 0x00, 0x07, 0x00, 0x00, 0xFE, 0x00, 0x00, 0x01, 0x00]
    select_aid = cmd_select + [len(aid)] + aid
    cc.send(select_aid)

    cmd_select_mf = [0x00, 0xA4, 0x00, 0x0C]
    cc.send(cmd_select_mf)

    cmd_select_dir = [0x00, 0xA4, 0x01, 0x0C]
    cc.send(cmd_select_dir + [0x02, 0x50, 0x00])

    cmd_select_dat = [0x00, 0xA4, 0x02, 0x0C]

    # Estonia ID1 Chip/App 2018 v1.0 page 17.
    esteid18_map = {
        1: "Surname",
        2: "First name",
        3: "Sex",
        4: "Citizenship",
        5: "Date and place of birth",
        6: "Personal identification code",
        7: "Document number",
        8: "Expiry date",
        9: "Date and place of issuance",
        10: "Type of residence permit",
        11: "Notes line 1",
        12: "Notes line 2",
        13: "Notes line 3",
        14: "Notes line 4",
        15: "Notes line 5",
    }

    # Fetch the personal data file.
    for k, v in esteid18_map.items():
        cc.send(cmd_select_dat + [0x02, 0x50, k])
        r = cc.send([0x00, 0xB0, 0x00, 0x00, 0x00])
        print(f"\t{v}:", bytes(r).decode())

    # Fetch PIN try counters.
    print("PIN try counters:")
    cc.send(cmd_select_mf)

    pin1 = cc.send([0x00, 0x20, 0x00, 0x01])
    puk = cc.send([0x00, 0x20, 0x00, 0x02])

    cc.send(cmd_select_dir + [0x02, 0xAD, 0xF2])
    pin2 = cc.send([0x00, 0x20, 0x00, 0x85])

    print("\tPIN1:", pin1 & 0x03, "left")
    print("\tPIN2:", pin2 & 0x03, "left")
    print("\tPUK :", puk & 0x03, "left")


if __name__ == "__main__":
    main()
