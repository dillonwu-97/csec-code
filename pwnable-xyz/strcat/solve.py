from pwn import *

r = process('./challenge')

gdb.attach(r)
r.sendafter(": ", "\x00") # name is 129 bytes long
r.sendafter(": ", "a" * 20)
r.recvuntil("> ")

# increment until the maxlen is 
for i in range(8):
    r.sendafter("k")


# overwrite malloc_ptr with your own pointer should be the goal i think
