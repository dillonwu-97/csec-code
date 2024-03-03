from pwn import *

r = process('./challenge')

r.sendafter(": ", "\x00")
r.sendafter(": ", "\x00")
r.recvuntil("> ")
gdb.attach(r)
