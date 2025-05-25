import sys

def main():
	with open ("to_flip.txt", "r") as tf:
		orig = []
		for i in tf.readlines():
			orig.append(i.rstrip())
	orig = [int(i) for i in orig]
	# print(orig)
	with open ("pp.txt", "r") as pp:
		primes = []
		for i in pp.readlines():
			primes.append(i.rstrip())
	primes = [int(i) for i in primes]
	xor = [primes[i] ^ orig[i] for i in range(40)]
	print(xor)
	ch = [chr(xor[i]) for i in range(40)]
	print("".join(ch))
	link = []
	for i in range(len(primes)):
		# print('primes is ', primes[i])
		# print('orig is ', orig[i])
		# print('xored val is ', primes[i] ^ orig[i])
		# print (chr(primes[i] ^ orig[i]))
		link.append(chr(primes[i] ^ orig[i]))
	print("".join(link))


if __name__ == '__main__':
	main()