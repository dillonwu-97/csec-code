from sympy.ntheory.modular import crt
import gmpy2
from Crypto.Util.number import long_to_bytes
from pwn import *
import json

r = remote('178.128.46.251',30600)
json_data = []
n = []
c = []
for i in range(5):
    r.recvuntil(') ')
    r.sendline('Y')
    j = json.loads(r.recvline())

    c.append(int(j["time_capsule"],16))
    n.append(int(j["pubkey"][0],16))

print("Solving...")

crt_val = crt(n, c)
gmpy2.get_context().precision=10000
print(crt_val[0])

m = gmpy2.root(crt_val[0], 5)
print(long_to_bytes(int(m)))