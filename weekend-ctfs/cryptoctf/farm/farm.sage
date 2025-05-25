#!/usr/bin/env sage

from sage.all import *
import string, base64, math


ALPHABET = string.printable[:62] + '\\='
flag = ALPHABET

F = list(GF(64))

def keygen(l):
	# l = 14
	# F[randint()] for _ in range(14)
	# multiply by the key 
	key = [F[randint(1, 63)] for _ in range(l)] 
	key = math.prod(key) # Optimization the key length :D
	return key

def maptofarm(c):
	assert c in ALPHABET
	return F[ALPHABET.index(c)]

def encrypt(msg, key):
	# m64 = base64.b64encode(msg)
	m64 = ALPHABET
	enc, pkey = '', key**5 + key**3 + key**2 + 1

	# pk = k^5 + k^3 + k^2 + 1; is this some irreducible polynomial?
	# get index of the alphabet
	# for each character in m64, do chr(m), and then map the character to some integer value?
	for m in m64:
		m = ord(m)
		print(F.index(pkey * maptofarm(chr(m))))
		print("pkey is: ", pkey)
		enc += ALPHABET[F.index(pkey * maptofarm(chr(m)))]

		# to reverse: ALPHABET[i], where i = F.index()
		# ALPHABET.index(c) = i
		# F[i] = random_pkey * something?
		# pkey = check all possible candidates
	return enc

# KEEP IT SECRET 
key = keygen(14) # I think 64**14 > 2**64 is not brute-forcible :P
# GF field 64 implies that it is closed

enc = encrypt(flag, key)
print(f'enc = {enc}')
