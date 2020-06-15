import sys
import math
import gmpy2
from decimal import *

# def prime_calc():

def solve_p(n):
	# getcontext().prec = 350
	# print ('test: ', n * 730 // 629)
	p = -1
	flag = 0
	for a in range(1,1001):
		print(a)
		# getcontext().prec=350
		# temp = Decimal(n) / Decimal(a)
		# print(int(temp))
		# if isinstance(temp, int):
		# 	print(temp)
		# 	break
		for b in range(1, 1001):
			p = gmpy2.isqrt((n * b) // a)
			# p = gmpy2.isqrt((n * b + 10000) // a)
			# if n% p == 0:
			# 	flag = 1
			# 	print(p)
			# 	break
			for i in range (-10, 10):
			# p = Decimal(n * b // a)
				temp = p + i
				# p = p.sqrt()
				# print(type(p))
				# print(n % p)
				if n % temp == 0:
					flag = 1
					print(temp)
					break
		if flag == 1:
			break

	
	return p
# 		# try: 
# 		print(decimal.Decimal(n * 1000 // i).sqrt())
# 		# except:
# 			# continue
# 	return 0


def xgcd(a, b):
    """return (g, x, y) such that a*x + b*y = g = gcd(a, b)"""
    x0, x1, y0, y1 = 0, 1, 1, 0
    while a != 0:
        (q, a), b = divmod(b, a), a
        y0, y1 = y1, y0 - q * y1
        x0, x1 = x1, x0 - q * x1
    return b, x0, y0

def split(msg, num):
	if num == 1:
		msg = list(msg)
		return msg[:-1]
	else:
		msg = ["0x" + msg[i:i+2] for i in range(0, len(msg), 2)]
		return msg[:-1]

def main():
	if len(sys.argv) < 1:
		systemexit()
	with open(sys.argv[1], "r") as f:
		inp = f.readlines()
		n = int(inp[1])
		e = int(inp[4])
		msg = inp[-1]
	# p = solve_p(n)
	# sys.exit()
	# After solving for p:
	p = 151086174643947302290817794140091756798645765602409645643205831091644137498519425104335688550286307690830177161800083588667379385673705979813357923016141205953591742544325170678167010991535747769057335224460619777264606691069942245683132083955765987513089646708001710658474178826337742596489996782669571549253
	print("p is ", p)
	q = n // p
	print("q is ", q)
	m = (p-1) * (q-1)
	print("m is ", m)
	x,d,y = xgcd(e, m)
	if (d < 0):
		d +=m
	print("d is ", d)
	print(x, y)
	# print(d * e + m * y)
	# use d to break code 
	# msg_1 = split(msg, 1)
	# msg_2 = split(msg, 2)
	# print(msg_1)
	# print(msg_2)
	# msg_2 = [int(i, 0) for i in msg_2 ]
	# print(msg_2)

	# print(pow(80, d, n))
	# ans = []
	# for i in msg_2:
		# temp = i ** y
		# ans.append(ord(str((pow(i, d, n)))))
	# print(ans)
	msg = "0x" + msg
	print(msg)
	msg = int(msg,16)
	print(msg)
	ans = hex(pow(msg, d, n))
	print(ans)
	ans = split(ans, 2)[1:]
	ans = [chr(int(i,0)) for i in ans]
	print(''.join(ans))





if __name__ == '__main__':
	main()