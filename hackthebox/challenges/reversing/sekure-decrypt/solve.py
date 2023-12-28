from pwn import *
import os
from Crypto.Cipher import AES

def find_enc(core, start_addr, end_addr):
    to_ret = []
    for i in range(start_addr, end_addr, 16):
        data = core.read(i, 16)
        if b'\x00' not in data:
            to_ret.append(data)
    return to_ret

def dec(ct):
    key = b'VXISlqY>Ve6D<{#F'
    iv = b'A' * 16
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = cipher.decrypt(ct)
    print("plaintext: ", pt)
    
def main():
#find_enc()
    core = Coredump('./core')
    for m in core.mappings:
        print(hex(m.start))
        print(hex(m.stop))
        print("*" * 10)
        to_check = find_enc(core, m.start, m.stop)
        for c in to_check:
            dec(c)

if __name__ == "__main__":
    # Flag: HTB{t1m_l3arn_C}
    main()
