from pwn import *
from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes
import hashlib

def encrypt(plaintext, shared_secret):
    key = hashlib.md5(long_to_bytes(shared_secret)).digest()
    cipher = AES.new(key, AES.MODE_ECB)
    message = cipher.encrypt(plaintext)
    return message

r = remote('142.93.32.153',30009)
r.recvuntil(": ")
r.sendline("1")
r.recvuntil(": ")
payload = encrypt(b"Initialization Sequence - Code 0", 1)
print(payload.hex())
r.interactive()
r.sendline(payload.hex())
print(r.recvline())
r.interactive()
# flag: HTB{7h15_15_cr3@t3d_by_Danb3er_@nd_h@s_c0pyr1gh7_1aws!_!}
