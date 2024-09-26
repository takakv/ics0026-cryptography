# Run with: sage rsa.sage

e = 65537
n = 230624063920680065513680711198246109591
c = 161670843286605628968182075437059446607

factors = n.factor()
p = factors[0][0]
q = factors[1][0]

phi = (p-1)*(q-1)
d = e.inverse_mod(phi)
m = c.powermod(d, n)

n_bytes = (m.nbits() + 1) // 8  # the min byte length to represent the number
# int(m) to get Python's methods to work since sage uses a custom implementation
# .to_bytes(..., "big") to get the actual bytes in Big Endian representation
# .decode() to UTF-8 decode the bytes
decoded = int(m).to_bytes(n_bytes, "big").decode()
print(decoded)
