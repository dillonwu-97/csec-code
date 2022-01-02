import gmpy2

def trans(x):
	return bytes.fromhex(hex(x)[2:])

# Determines if n is a quadratic residue of an 
# odd prime p by using Euler's criterion.
def is_quadratic_residue(n, p):
	if n % p == 0:
		return True
	return pow(n, (p - 1)//2, p) == 1

def tonelli_shanks(n,p):
		# Case when p|n, so n=0(mod p). The square root of 0 is 0. 
	if n % p == 0:
		return 0
	
	# So now p=1(mod 4), (although this is not needed in the algorithm).
	# Write p - 1 = (2^S)(Q) where Q is odd
	Q = p - 1
	S = 0
	while Q % 2 == 0:
		S += 1
		Q //= 2
	# print("Q=", Q)
	# print("S=", S)

	# Find a quadratic non-residue of p by brute force search
	z = 2
	while is_quadratic_residue(z, p):
		z += 1
	# print("z=", z)

	# Initialize variables
	M = S
	c = pow(z, Q, p)
	t = pow(n, Q, p)
	R = pow(n, (Q + 1)//2, p)
	
	while t != 1:

		# Calculate i
		i = 0
		temp = t 
		while temp != 1:
			i += 1
			temp = (temp * temp) % p
		
		# Calculate b, M, c, t, R
		pow2 = 2 ** (M - i - 1)
		b = pow(c, pow2, p)
		M = i
		c = (b * b) % p
		t = (t * b * b) % p
		R = (R * b) % p

	# We have found a square
	return R

def broken_rsa():
	n = 27772857409875257529415990911214211975844307184430241451899407838750503024323367895540981606586709985980003435082116995888017731426634845808624796292507989171497629109450825818587383112280639037484593490692935998202437639626747133650990603333094513531505209954273004473567193235535061942991750932725808679249964667090723480397916715320876867803719301313440005075056481203859010490836599717523664197112053206745235908610484907715210436413015546671034478367679465233737115549451849810421017181842615880836253875862101545582922437858358265964489786463923280312860843031914516061327752183283528015684588796400861331354873
	e = 16
	ct = 11303174761894431146735697569489134747234975144162172162401674567273034831391936916397234068346115459134602443963604063679379285919302225719050193590179240191429612072131629779948379821039610415099784351073443218911356328815458050694493726951231241096695626477586428880220528001269746547018741237131741255022371957489462380305100634600499204435763201371188769446054925748151987175656677342779043435047048130599123081581036362712208692748034620245590448762406543804069935873123161582756799517226666835316588896306926659321054276507714414876684738121421124177324568084533020088172040422767194971217814466953837590498718

	### Testing ideas
	# print(is_quadratic_residue(ct, n)) # True
	# p8 = tonelli_shanks(ct, n) # (p^8) ^ 2 cong c mod n; p^8 =p8
	# # possible p value is now 
	# print(p8)
	# print(is_quadratic_residue(p8, n)) # p8 is also a quadratic residue

	# assert( p8**2 % n == ct)
	# p4 = tonelli_shanks(p8, n)
	# assert(p4 ** 4 % n == ct)

	pstart = ct
	while (e != 1):
		pstart = tonelli_shanks(pstart, n)
		e//=2
	assert(pstart ** 16 % n == ct)
	print(trans(-pstart%n))
	

def successive_powers():
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



def main():
	broken_rsa()

if __name__ == '__main__':
	main()

