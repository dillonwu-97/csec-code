'''
Byte-at-a-time ECB decryption (Simple)
Copy your oracle function to a new function that encrypts buffers under ECB mode using a consistent but unknown key (for instance, assign a single random key, once, to a global variable).

Now take that same function and have it append to the plaintext, BEFORE ENCRYPTING, the following string:

Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg
aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq
dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg
YnkK
Spoiler alert.
Do not decode this string now. Don't do it.

Base64 decode the string before appending it. Do not base64 decode the string by hand; make your code do it. The point is that you don't know its contents.

What you have now is a function that produces:

AES-128-ECB(your-string || unknown-string, random-key)
It turns out: you can decrypt "unknown-string" with repeated calls to the oracle function!

Here's roughly how:

Feed identical bytes of your-string to the function 1 at a time --- start with 1 byte ("A"), then "AA", then "AAA" and so on. Discover the block size of the cipher. You know it, but do this step anyway.
Detect that the function is using ECB. You already know, but do this step anyways.
Knowing the block size, craft an input block that is exactly 1 byte short (for instance, if the block size is 8 bytes, make "AAAAAAA"). Think about what the oracle function is going to put in that last byte position.
Make a dictionary of every possible last byte by feeding different strings to the oracle; for instance, "AAAAAAAA", "AAAAAAAB", "AAAAAAAC", remembering the first block of each invocation.
Match the output of the one-byte-short input to one of the entries in your dictionary. You've now discovered the first byte of unknown-string.
Repeat for the next byte.
Congratulations.
This is the first challenge we've given you whose solution will break real crypto. Lots of people know that when you encrypt something in ECB mode, you can see penguins through it. Not so many of them can decrypt the contents of those ciphertexts, and now you can. If our experience is any guideline, this attack will get you code execution in security tests about once a year.
'''
import os
import binascii
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import random
from collections import Counter

######################################## Encryption ########################################
def randBytes(size):
	return os.urandom(size)

def encrypt_ecb(plaintext, key):
	plaintext = plaintext + randBytes(16 - len(plaintext) % 16) # padding
	cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
	encryptor = cipher.encryptor()
	encrypted = encryptor.update(plaintext) + encryptor.finalize()
	return encrypted

######################################## Find Block Size ########################################
# How to find block size of cipher?
# To find block size, vary the parameter block_size until a repeat is identified
def findBlockSize(encrypted_data):
	hex_encrypt = encrypted_data.hex()
	block_prediction = -1
	for block_size in range(1,64):
		d = {}	
		for count in range(0, block_size*2+1, block_size * 2):
			# 2 * block_size because hex takes up 2 characters for each byte
			if hex_encrypt[count:count+ 2*block_size] not in d:
				d[ hex_encrypt[count:count+2* block_size] ] = 1
			else:
				block_prediction = block_size
				break
	print('Block Size prediction is ', block_prediction)


##### Good explanation of the attack: https://crypto.stackexchange.com/questions/55673/why-is-byte-at-a-time-ecb-decryption-a-vulnerability
def main():
	key = randBytes(16)
	s = 'Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK'
	
################################### Finding Block Size ###################################
	p = 'A' * 48
	# print(base64.b64decode('eW91ciB0ZXh0')) # checking b64 syntax
	ciphertext = encrypt_ecb(p.encode() + base64.b64decode(s), key)

	# Identifying the block size
	findBlockSize(ciphertext)
################################### Cracking secret value s ###################################

	# 32-127 is standard ascii range
	# Not sure how to find the next 16 characters
	block = "A"*15 # this is used to deduce the next character
	p = 'A' * 15
	start = 0
	end = 1
	ciphertext = encrypt_ecb(p.encode() + base64.b64decode(s), key)
	s_solved = ""
	while (16 * end < len(ciphertext)):
		if (len(p) == 0): 
			# print("new start and end ", start, end)
			start +=1
			end+=1
			p = 'A' * 16
		# print(count, block)
		print(block)
		ciphertext = encrypt_ecb(p.encode() + base64.b64decode(s), key)
		for i in range(128):
			temp = block + chr(i)
			val = encrypt_ecb(temp.encode(), key)
			# shift the ciphertext being compared
			if (val[:16] == ciphertext[16*start:16*end]):
				block = temp[1:]
				p = p[1:]
				s_solved += temp[-1]
				break
	print(s_solved[:-1]) # ignore last character
if __name__ == '__main__':
	main()













