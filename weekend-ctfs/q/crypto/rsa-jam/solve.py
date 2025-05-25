# NOTE: Not sure why lcm works
import gmpy2
from pwn import *
import ast
import math

# solution: 
# step 1) https://stackoverflow.com/questions/2921406/calculate-primes-p-and-q-from-private-exponent-d-public-exponent-e-and-the
# step 2) https://crypto.stackexchange.com/questions/48828/multiple-private-keys-with-rsa

def findpq(d, e, N):
    ed = e * d
    gmpy2.get_context().precision=10000
    # my_ed * d = phi(n) * k + 1
    # print (my_e * d - 1) # <-- this is a multiple of phi(n)
    # the range is 1 -> e for k 
    p = -1
    q = -1
    for k in range(1, e):
        temp = (ed-1)
        if temp % k == 0:
            temp //= k # phi(n) possibility
            p_plus_q = N + 1 - temp
            # ((p+q) + sqrt((p+q)2 - 4*pq))/2
            sqrt_check = gmpy2.is_square( pow(p_plus_q, 2) - 4 * N)
            if sqrt_check == True:
                # p = ((p+q) + sqrt((p+q)2 - 4*pq))/2
                # q = ((p+q) - sqrt((p+q)2 - 4*pq))/2
                p = (p_plus_q + gmpy2.sqrt( pow(p_plus_q, 2) - 4 * N)) //2
                p = int(p)
                q = (p_plus_q - gmpy2.sqrt( pow(p_plus_q, 2) - 4 * N)) //2
                q = int(q)

    return p, q

def lcm(x, y):
    from math import gcd # or can import gcd from `math` in Python 3
    return x * y // gcd(x, y)

def main():
	# Testing to make sure it works
	# dic = {'e': 65537, 'd': 31350137288109501809894295350232647207093323581338285335918035883198258781665089375302287197546240417099641687446703629763343814011373518310298923570866000443524764411091719481693280275361801175393006731265353320409157634751938347167384362688798600314309722311587201478131468566768230237542049426596645996145, 'N': 114125087343822275182749676963183747153878528442491096265070283712557034148418872542864300175836691563376060504926657545064726075590922972254738685444861715133322090016558967845654398854797976188423796216660172610534196472439789614238790304335326996611931195105075973557055661851113506892638093089156629967193}
	# d = dic['d']
	# e = dic['e']
	# N = dic['N']
	# p, q = findpq(d, e, N)

	# assert( p * q == N)
	# phi = (p-1) * (q-1)
	# d2 = phi + d

	# m = 10 
	# c = pow(m, e, N)

	# d2 = lcm(p-1, q-1)
	# d2 = gmpy2.invert(e, d2)
	# # d2 = gmpy2.invert(e, phi * 3)
	# assert (d2 < phi)
	# m1 = pow(c, d2, N)
	# # print(m, m1)
	# assert(m == m1)
	# assert(d != d2)
	

	


	r = remote('138.68.182.108', 31988)
	r.recvline()
	a = r.recvline()
	dict_str = a.decode("UTF-8")
	dic = ast.literal_eval(dict_str)
	
	d = dic['d']
	e = dic['e']
	N = dic['N']
	p, q = findpq(d, e, N)
	assert (p * q == N)
	phi = (p-1) * (q-1)

	d2 = lcm(p-1, q-1)
	d2 = gmpy2.invert(e, d2)

	a = r.recvuntil("> ")
	print(a)
	# a = r.sendline("10")
	# print(a)
	assert(d2 < phi)
	a = r.sendline(str(d2))
	print(a, str(d2))
	# a = r.recvuntil("AssertionError")
	a = r.recvline()
	print(a)
	# CHTB{lambda_but_n0t_lam3_bda}

if __name__ == '__main__':
	main()