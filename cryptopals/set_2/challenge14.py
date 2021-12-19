'''
Take your oracle function from #12. Now generate a random count of random bytes and prepend this string to every plaintext. You are now doing:

AES-128-ECB(random-prefix || attacker-controlled || target-bytes, random-key)
Same goal: decrypt the target-bytes.
'''

import os
import random
import binascii
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from collections import Counter
import random

def randBytes(size):
	return os.urandom(size)

def encrypt_ecb(plaintext, key):
	plaintext = plaintext + randBytes(16 - len(plaintext) % 16) # padding
	cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
	encryptor = cipher.encryptor()
	encrypted = encryptor.update(plaintext) + encryptor.finalize()
	return encrypted

def main():
################################### Setup ###################################
	key = randBytes(16)
	s = 'Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK'
	s_bytes = base64.b64decode(s)
################################### Cracking secret value s ###################################
	prefix = randBytes(random.randint(1,5))
	p = 15 * "A" # padding
	p_count = 15
	payload = p.encode() + base64.b64decode(s) # new string to encode of the form (random-prefix || attacker-controlled || target-bytes)
	ciphertext = encrypt_ecb(prefix + payload, key)

	# Idea is to use 16 "A"s and to keep decreasing the number of "A"s in order to find the prefix size
	# Once you have the prefix size, the steps will be the same as challenge12
	############################## Finding prefix size ##############################
	comparison_block = encrypt_ecb(prefix + (16 * "A").encode(), key)
	while (ciphertext[:16] == comparison_block[:16]):
		payload = payload[1:]
		p_count-=1
		ciphertext = encrypt_ecb(prefix + payload, key)
	prefix_byte_size = 15 - p_count
	print("Prefix size is", prefix_byte_size)

	############################## Using the method from challenge12 to solve this problem ##############################
	block = (15-prefix_byte_size) * "A"
	payload = (15-prefix_byte_size) * "A"
	start = 0
	shift_size = 15-prefix_byte_size # after first round, shift size becomes 16 because in the first round, we can only handle 10 characters
	prev = " " # keep track of when ret value stops updating
	ret = ""
	while(ret != prev):
		if start != 0:
			prev = ret
			block = "A" * (16-prefix_byte_size + (16 * start-1)-len(ret))
			payload = "A" * (16-prefix_byte_size + (16 * start - 1)-len(ret)) + ret
			shift_size = 16
		for j in range(shift_size):
			crackme = encrypt_ecb(prefix + block.encode() + s_bytes, key) # compare our ciphertext with this
			for i in range(128):
				temp = payload + chr(i)
				# print(temp)
				ciphertext = encrypt_ecb(prefix + temp.encode() + s_bytes, key)
				# print(ciphertext[:16], crackme[:16])
				if (ciphertext[start * 16: (start + 1) * 16] == crackme[start * 16: (start + 1) * 16]):
					ret += chr(i)
					payload = temp[1:]
					block = block[1:]
					break
		start +=1
		# print("next ", ret)
		# print(len(ret))
	print(ret[:-1])	 #ignore last byte		

	############################## Sandbox for testing ##############################
	# block = (15-prefix_byte_size) * "A" # including the prefix, the size of the payload will be 15, which leaves 1 char for manipulation
	# # print("Payload size is ", len(payload) + len(prefix))
	# payload = (15-prefix_byte_size) * "A"
	# ret = ""
	# start = 0

	# # Find all the characters that are retrievable and then shift over to the next block
	# # block = ((15-prefix_byte_size) + start * 16) * "A"
	# ##### This is used to find the next few characters after the first round
	# ##### General formula for this is: block = "A" * (11 + 16 * start - len(ret) - 1)
	# ##### payload = "A" * (11 + 16 * start - len(ret) - 1) + ret
	# block = "A" * (11 + 15-len("Rollin' i")) 
	# payload="A" * (11 + 15-len("Rollin' i")) + "Rollin' i"
	# print(len(block) + 5 + len("Rollin' i")) 
	# for j in range(len(block)):
	# 	# print(payload)
	# 	crackme = encrypt_ecb(prefix + block.encode() + s_bytes, key) # compare our ciphertext with this
	# 	for i in range(128):
	# 		temp = payload + chr(i)
	# 		# print(temp)
	# 		ciphertext = encrypt_ecb(prefix + temp.encode() + s_bytes, key)
	# 		# print(ciphertext[:16], crackme[:16])
	# 		if (ciphertext[16:32] == crackme[16:32]):
	# 			ret += chr(i)
	# 			payload = temp[1:]
	# 			block = block[1:]
	# 			break
	# print(ret)
	# start += 1
	# print(len(ret), ret)
	# print(payload, len(payload))






if __name__ == '__main__':
	main()




