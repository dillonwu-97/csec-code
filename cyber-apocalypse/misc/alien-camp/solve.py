from pwn import *

def showline(r):
	a = r.recvline()
	print(a)

def calculate(s, d):
	print(s)
	s = "+" + s
	stack = []
	for i in range(0, len(s),2):
		if s[i] == '+':
			stack.append(d [s[i+1]] )
		elif s[i] == '-':
			stack.append(- d[s[i+1] ])
		elif s[i] == '*':
			stack.append(stack.pop() * d[s[i+1]])
		elif s[i] == '/':
			stack.append(stack.pop() // d[s[i+1]])
		elif s[i] == "=":
			break
	return sum(stack)
	

def solve(r, d):
	r.recvuntil(":\n\n")
	a = r.recvline()
	a = a.decode().strip().split(" ")
	ret = calculate( "".join(a), d)
	ret = str(ret)
	r.recvuntil("Answer: ")
	r.sendline(ret)


def main():
	host = '165.227.237.7'
	port = 30316
	r = remote(host, port)
	r.recvuntil("> ")
	r.sendline("1")
	r.recvline()
	r.recvline()
	a = r.recvline()
	translate = a.decode().strip().split(" ")
	translate = [i for i in translate if i!="->"]
	d = {}
	for i in range(0, len(translate), 2):
		d[translate[i]] = int(translate[i+1])
	print(d)

	a = r.recvuntil("> ")
	print(a)
	r.sendline("2")
	
	
	# print("hi")
	for i in range(500):
		solve(r, d)

	for i in range(10):
		showline(r)
	

	

if __name__ == '__main__':
	main()
	# CHTB{3v3n_4l13n5_u53_3m0j15_t0_c0mmun1c4t3}