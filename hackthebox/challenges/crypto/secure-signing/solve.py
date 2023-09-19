from pwn import *
from hashlib import sha256

r = remote('206.189.121.78', 30873)


# Attack is to just leak the 0's
def H(m):
    return sha256(m).digest()

def xor(a, b):
    return bytes([i ^ j for i, j in zip(a, b)])

def sign(m: string):
    r.recvuntil("> ")
    r.sendline("1")
    r.recvuntil(": ")
    r.sendline(m)
    hash = r.recvline().decode().strip("\n").split(": ")[1]
    return hash

def verify(m: string, h: string):
    r.recvuntil("> ")
    r.sendline("2")
    r.recvuntil(": ")
    r.sendline(m)
    r.recvuntil(": ")
    r.sendline(h)
    l = r.recvline()
    if "Validated" in l:
        return True
    else:
        return False

def main():

    zpreimage = b'\x00'
    zhash = H(zpreimage).hex()
    flag = ""

    to_send = b''
    while 1: 
        for i in range(32, 129):
            temp = to_send + i.to_bytes(1, 'big')
            print("Sending: ", temp)
            temp2 = sign(temp)
            if temp2 == zhash:
                flag += chr(i)
                print("Found!", flag)
                to_send = flag.encode()
                zpreimage += b'\x00'
                zhash = H(zpreimage).hex()
                break
            else:
                print("nope")

if __name__ == '__main__':
    main()
    # Flag: HTB{r0ll1n6_0v3r_x0r_w17h_h@5h1n6_0r@cl3_15_n07_s3cur3!@#}