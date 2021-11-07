import random
from pwn import *
import _thread

def solve(buffer):

	host = '178.128.160.242'
	port = 30369

	p = remote(host, port)

	p.recvuntil("Put here the next 5 numbers: ")

	seed = int(time.time()) -5
	

	extracted = []
	next_five = []

	# Initialize the (pseudo)random number generator
	random.seed(seed)
	
	# First extraction
	while len(extracted) < 5:
		r = random.randint(1, 90)
		if(r not in extracted):
			extracted.append(r)
			
	# Next extraction
	solution = ""
	while len(next_five) < 5:
		r = random.randint(1, 90)
		if(r not in next_five):
			next_five.append(r)
			solution += str(r) + " "
	solution = solution.strip()

	print("seed is: ", seed)
	print(solution)
	
	p.sendline(solution)
	a = p.recvline()
	a = p.recvline()
	print(a)

#flag: HTB{n3v3r_u53_pr3d1c74bl3_533d5_1n_p53ud0-r4nd0m_numb3r_63n3r470r}

def main():
	# for i in range(-20,20,1):
	# 	print(i)
	# 	_thread.start_new_thread(solve, (i,))

	solve(1)


if __name__ == '__main__':
	main()
