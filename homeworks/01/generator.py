import secrets

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

msg = "Good job on recovering the message!"
padded = pad(msg.encode(), AES.block_size)

key = secrets.token_bytes(16)
cipher = AES.new(key, AES.MODE_CBC, key)
ct = cipher.encrypt(padded)

print(ct.hex())

b1 = ct[:AES.block_size]
b2 = ct[:AES.block_size]

print(secrets.token_bytes(32).hex())