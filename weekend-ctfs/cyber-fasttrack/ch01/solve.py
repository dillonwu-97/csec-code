from Crypto.PublicKey import RSA
import base64
# from sympy.solvers.diophantine.diophantine import base_solution_linear
from sympy.solvers.diophantine import base_solution_linear
import gmpy2

def main():
	f = open('1.pub')
	pk1 = RSA.importKey(f.read())

	f = open('2.pub')
	pk2 = RSA.importKey(f.read())

	print('-' * 10 + "pk1 info" + '-' * 10)
	print("e ", pk1.e)
	print("m ", pk1.n)

	print('-' * 10 + "pk2 info" + '-' * 10)
	print("e ", pk2.e)
	print("m ", pk2.n)


	f = open('m1.enc')
	m1 = base64.b64decode(f.read()).hex()

	f = open('m2.enc')
	m2 = base64.b64decode(f.read()).hex()

	print('-' * 10 + "m1 is " + '-' * 10)
	print(m1)

	print('-' * 10 + "m2 is " + '-' * 10)
	print(m2)


	e1 = pk1.e
	e2 = pk2.e
	n = pk1.n
	sol = base_solution_linear(1,e1,-e2)
	x = int(sol[0])
	y = -int(sol[1] )
	# print(x, y)

	m1 = int(m1,16)
	m2 = int(m2, 16)
	
	# print(e1 * x + e2 * y) # double checking

	message = (pow(m1, x, n) * pow(gmpy2.invert(m2, n), -y, n)) % n
	print(message)

	s = hex(message)[2:]
	b = bytes.fromhex(s)
	print(b.decode("ascii"))



if __name__ == '__main__':
	main()