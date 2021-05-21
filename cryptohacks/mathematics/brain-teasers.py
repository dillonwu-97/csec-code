import gmpy2


# https://math.stackexchange.com/questions/2367841/what-is-the-best-way-to-solve-modular-arithmetic-equations-such-as-9x-equiv-33
prime_list = [ 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]
x_n1 = 588 # x^n
x_n2 = 665 # x^2n
x_n3 = 216 # x^3n
for p in prime_list:
	temp = gmpy2.invert(x_n1, p)
	x = (temp * x_n2) % p
	print(p, x)
	if (x_n1 * x * x) % p == x_n3:
		print("solved", p,x)