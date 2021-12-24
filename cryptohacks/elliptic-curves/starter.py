import gmpy2
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib


# Algorithm for the addition of two points: P + Q
# Formula: Y2 = X3 + a X + b
# (a) If P = O, then P + Q = Q.
# (b) Otherwise, if Q = O, then P + Q = P.
# (c) Otherwise, write P = (x1, y1) and Q = (x2, y2).
# (d) If x1 = x2 and y1 = −y2, then P + Q = O.
# (e) Otherwise:
#   (e1) if P ≠ Q: λ = (y2 - y1) / (x2 - x1)
#   (e2) if P = Q: λ = (3x12 + a) / 2y1
# (f) x3 = λ2 − x1 − x2,     y3 = λ(x1 −x3) − y1
# (g) P + Q = (x3, y3)
def point_addition(p, q, a, prime):
	if p == 0:
		return q
	if q == 0:
		return p
	x1, y1 = p
	x2, y2 = q
	if x1 == x2 and y1 == -y2:
		return (0,0)
	if p != q:
		l = (y2 - y1) * pow(x2 - x1,-1, prime)
		l %= prime
	elif p == q:
		l = (3 * x1 ** 2 + a) * pow(2 * y1,-1, prime)
		l %= prime
	x3 = l**2 - x1 - x2
	x3 %= prime
	y3 = l *(x1 - x3) - y1
	y3 %= prime
	return (x3, y3)

# Double and Add algorithm for the scalar multiplication of point P by n

# Input: P in E(Fp) and an integer n > 0
# 1. Set Q = P and R = O.
# 2. Loop while n > 0.
#   3. If n ≡ 1 mod 2, set R = R + Q.
#   4. Set Q = 2 Q and n = ⌊n/2⌋.
#   5. If n > 0, continue with loop at Step 2.
# 6. Return the point R, which equals nP.

def scalar_mult(P, n, a, p):
	Q = P
	R = 0
	while (n >= 1):
		if n % 2 == 1:
			R = point_addition(R, Q, a, p)
		Q = point_addition(Q, Q, a, p)
		n //= 2

	return R

def is_pkcs7_padded(message):
	padding = message[-message[-1]:]
	return all(padding[i] == len(padding) for i in range(0, len(padding)))


def decrypt_flag(shared_secret: int, iv: str, ciphertext: str):
	# Derive AES key from shared secret
	sha1 = hashlib.sha1()
	sha1.update(str(shared_secret).encode('ascii'))
	key = sha1.digest()[:16]
	# Decrypt flag
	ciphertext = bytes.fromhex(ciphertext)
	iv = bytes.fromhex(iv)
	cipher = AES.new(key, AES.MODE_CBC, iv)
	plaintext = cipher.decrypt(ciphertext)

	if is_pkcs7_padded(plaintext):
		return unpad(plaintext, 16).decode('ascii')
	else:
		print(plaintext)
		return plaintext.decode('ascii')




def main():
	# 1. Point Negation
	# Y2 = X3 + 497 X + 1768
	# P(8045,6936) Q(x,y) P + Q = 0
	p = 9739
	Px = 8045
	Py = 6936
	print(Py**2 % p, (Px**3 + 497 * Px + 1768) % p)
	# assert (Py**2 == (Px**3 + 497 * Px + 1768))
	# Flag: crypto{8045,2803}

	# 2. Point Addition
	# P = (493, 5564), Q = (1539, 4742), R = (4403,5202)
	# S(x,y) = P + P + Q + R 
	P = (493, 5564)
	Q = (1539, 4742)
	R = (4403, 5202)
	x = point_addition(P, P, 497, p)
	y = point_addition(x, Q, 497, p)
	z = point_addition(y, R, 497, p)
	print(z)
	# Flag: crypto{4215,2162}

	# 3. Scalar Multiplication
	P = (2339, 2213)
	n = 7863 
	print(scalar_mult(P, n, 497, p))
	# Flag: crypto{9467, 2742}

	# 4. Curves and Logs
	# E: Y2 = X3 + 497 X + 1768, p: 9739, G: (1804,5368)
	# QA = (815, 3190), with your secret integer nB = 1829
	Qa = (815, 3190)
	nb = 1829
	s = scalar_mult(Qa, nb, 497, 9739)
	hash_obj = hashlib.sha1(str(s[0]).encode()).hexdigest()
	print(hash_obj)
	# Flag: crypto{80e5212754a824d3a4aed185ace4f9cac0f908bf}

	# 5. Efficient Exchange
	# Y2 = X3 + 497 X + 1768
	# helpful for finding square root of quadratic residue:
	# https://math.stackexchange.com/questions/1603885/how-to-get-all-solutions-of-x2-equiv-a-mod-p
	d = {'iv': 'cd9da9f1c60925922377ea952afc212c', 'encrypted_flag': 'febcbe3a3414a730b125931dccf912d2239f3e969c4334d95ed0ec86f6449ad8'}
	iv = d['iv']
	c = d['encrypted_flag']
	q_x = 4726
	nB = 6534
	q_y2 = (q_x ** 3 + 497 * q_x + 1768) % 9739
	# some value y | y * y % 9739 = y^2
	k = (p - 3) // 4
	q_y = q_y2 ** (k + 1) % p
	s = scalar_mult((q_x, q_y), nB, 497, 9739)
	print(s)
	print(decrypt_flag(s[0], iv, c))
	# Flag: crypto{3ff1c1ent_k3y_3xch4ng3}








if __name__ == '__main__':
	main()