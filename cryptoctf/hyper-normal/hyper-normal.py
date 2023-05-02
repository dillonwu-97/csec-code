#!/usr/bin/env python3

import random
from flag import FLAG

p = 8443

# does a transpose
def transpose(x):
	result = [[x[j][i] for j in range(len(x))] for i in range(len(x[0]))]
	return result

# Take the sum of two arrays / vectors
def vsum(u, v):
	assert len(u) == len(v)
	l, w = len(u), []
	for i in range(l):
		w += [(u[i] + v[i]) % p]
	return w

# For each element in the array, multiply by some value a and take the modulo 
def sprod(a, u):
	w = []
	for i in range(len(u)):
		w += [a*u[i] % p]
	return w

def encrypt(msg):
	l = len(msg)

	# 
	hyper = [ord(m)*(i+1) for (m, i) in zip(list(msg), range(l))]

	# Not sure what V and W are 

	V, W = [], []
	for i in range(l):
		v = [0]*i + [hyper[i]] + [0]*(l - i - 1)
		V.append(v)
	random.shuffle(V)

	# grab a random integer from range 0->126 = R 
	# all 0's in v
	# take the vector sum of [0]'s and the product of R and V
	# take the vector sum of [0]'s and the product of R array and V array? 
	for _ in range(l):
		R, v = [random.randint(0, 126) for _ in range(l)], [0]*l
		for j in range(l):
			v = vsum(v, sprod(R[j], V[j]))
		W.append(v)

	# transpose W matrix and then shuffle? 
	# how does shuffle work exactly 
	random.shuffle(transpose(W))
	return W

enc = encrypt(FLAG)
print(enc)
