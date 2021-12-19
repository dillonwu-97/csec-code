'''
In this file are a bunch of hex-encoded ciphertexts.

One of them has been encrypted with ECB.

Detect it.

Remember that the problem with ECB is that it is stateless and deterministic; the same 16 byte plaintext block will always produce the same 16 byte ciphertext.
'''
from collections import Counter
def main():

	encrypted = []
	with open('file.txt', 'r') as f:
		for i in f:
			encrypted.append(i.strip('\n'))

	for count, text in enumerate(encrypted):
		d = {}
		for j in range(len(text)-16):
			if text[j:j+16] not in d:
				d[ text[j:j+16] ] = 1
			else:
				print('found a repeat in the ciphertext: ', text, ' in position ', count) 
				break


if __name__ == '__main__':
	main()