from sympy.solvers.diophantine.diophantine import base_solution_linear
import base64
import gmpy2
from fractions import gcd
import binascii
def main():
	e1 = 65537
	e2 = 343223
	sol = base_solution_linear(1,e1,-e2)
	# x = sol[0] # 133132 
	# y = sol[1] # -25421
	x = 133132
	y = -25421

	# print(x, y)

	c1_b64 = 'RBVdQw7Pllwb42GDYyRa6ByVOfzRrZHmxBkUPD393zxOcrNRZgfub1mqcrAgX4PAsvAOWptJSHbrHctFm6rJLzhBi/rAsKGboWqPAWYIu49Rt7Sc/5+LE2dvy5zriAKclchv9d+uUJ4/kU/vcpg2qlfTnyor6naBsZQvRze0VCMkPvqWPuE6iL6YEAjZmLWmb+bqO+unTLF4YtM1MkKTtiOEy+Bbd4LxlXIO1KSFVOoGjyLW2pVIgKzotB1/9BwJMKJV14/+MUEiP40ehH0U2zr8BeueeXp6NIZwS/9svmvmVi06Np74EbL+aeB4meaXH22fJU0eyL2FppeyvbVaYQ==' 
	c2_b64 = 'TSHSOfFBkK/sSE4vWxy00EAnZXrIsBI/Y6mGv466baOsST+qyYXHdPsI33Kr6ovucDjgDw/VvQtsAuGhthLbLVdldt9OWDhK5lbM6e0CuhKSoJntnvCz7GtZvjgPM7JDHQkAU7Pcyall9UEqL+W6ZCkiSQnK+j6QB7ynwCsW1wAmnCM68fY2HaBvd8RP2+rPgWv9grcEBkXf7ewA+sxSw7hahMaW0LYhsMYUggrcKqhofGgl+4UR5pdSiFg4YKUSgdSw1Ic/tug9vfHuLSiiuhrtP38yVzazqOZPXGxG4tQ6btc1helH0cLfw1SCdua1ejyan9l1GLXsAyGOKSFdKw=='

	c1_hex = base64.b64decode(c1_b64).hex()
	c2_hex = base64.b64decode(c2_b64).hex()
	# print("c1 hex is: ")
	# print(c1_hex)
	# print("c2 hex is: ")
	# print(c2_hex)

	c1_int = int(c1_hex, 16)
	c2_int = int(c2_hex, 16)
	# print("c1 int is: ")
	# print(c1_int)
	# print("c2 int is: ")
	# print(c2_int)

	# the modulo
	n = 'c6acb8df486e6671d4a5564803e1c3214a8e274de0ac0043ec28c8589f377c7e8d308bc3e302850384344ba7988885620a418e6ad955578284fc04f289f126b38a01816251cef9a14fd4c249d96b69087fa91b2e1adbdc80cb96ff0ccb6129d8f6737da850c451f2ed3f6cb61c36891dc924d0ab28f26adf0ed357ce848d02ffe00912714ccf6372c1f41080e86747a0303eb5cdf6ce912f1144fd4f55743c796875a14fdff8f8b662150c56be58b09239771dc44d969079c4ad8fd993bc630b7855d2e02e8be16824dcd5ab3813231c1731110a8bd028d7a1dfab892e75294557bafc71aeaf5e48db0267a6db63d350f995068ee1cad6d32df11a49bd24ba97'
	# note: .hex() only converts int to hex, not bytes
	n = int(n, 16)
	# print(e1 * x + e2 * y) # double checking

	message = (pow(c1_int, x, n) * pow(gmpy2.invert(c2_int, n), -y, n)) % n
	print(message)

	s = hex(message)[2:]
	b = bytes.fromhex(s)
	print(b.decode("ascii"))

if __name__ == '__main__':
	main()