import hashlib
import hmac


class Authenticator:
    _seen: set[bytes] = set()

    def __init__(self, key: bytes):
        self._key = key

    def authenticate(self, nonce: bytes, mac: str) -> tuple[bool, str]:
        """Authenticate a user by verifying a nonce and its MAC.

        If the nonce has already been used for authentication, the
        authentication fails.

        :param nonce: The nonce to use for authenticating
        :param mac: The MAC: a sha256 hex string
        :return: whether the authentication was successful and a status message
        """
        if nonce in self._seen:
            return False, "[!] Error: nonce already used"

        self._seen.add(nonce)
        if not hmac.compare_digest(self._compute_mac(nonce), mac):
            return False, "[!] Error: credentials not valid"
        return True, "[+] Login successful"

    def _compute_mac(self, data: bytes) -> str:
        return hashlib.sha256(self._key + data).hexdigest()
