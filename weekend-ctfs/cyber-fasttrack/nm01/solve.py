from pwn import *

def solve(a):
	ret = ''

	for i in range(0,len(a),4):
		try:
			temp = int(a[i+2:i+4].lower(),16)
			temp = chr(temp)
			# print(temp)
			ret += temp
		except:
			return ret
	return ret

def main():
	r = remote('cfta-nm01.allyourbases.co', 8017)
	# while(1):
	l = r.recvline().decode()
	# print(l)
	l = solve(l)
	r.send(l + '\n')
	# print(l)
	# l = r.recvline()
	r.interactive()
	# print(l)	

if __name__ == '__main__':
	main()

