'''
An ECB/CBC detection oracle
Now that you have ECB and CBC working:

Write a function to generate a random AES key; that's just 16 random bytes.

Write a function that encrypts data under an unknown key --- that is, a function that generates a random key and encrypts under it.

The function should look like:

encryption_oracle(your-input)
=> [MEANINGLESS JIBBER JABBER]
Under the hood, have the function append 5-10 bytes (count chosen randomly) before the plaintext and 5-10 bytes after the plaintext.

Now, have the function choose to encrypt under ECB 1/2 the time, and under CBC the other half (just use random IVs each time for CBC). Use rand(2) to decide which to use.

Detect the block cipher mode the function is using each time. You should end up with a piece of code that, pointed at a block box that might be encrypting ECB or CBC, tells you which one is happening.
'''
import os
import binascii
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import random
from collections import Counter

def randBytes(size):
	return os.urandom(size)

def encryptData(to_encrypt):
	rk = randBytes(16) # key
	append_before = randBytes(random.randint(5, 10))
	to_encrypt_bytes = append_before + to_encrypt.encode() # bytes to encrypt
	to_encrypt_bytes += randBytes(16 - (len(to_encrypt_bytes) % 16)) # add padding as well
	print("to encrypt: ", to_encrypt_bytes, len(to_encrypt_bytes))

################################### ECB mode #########################
	cipher_ECB = Cipher(algorithms.AES(rk), modes.ECB(), backend=default_backend())
	encryptor_ECB = cipher_ECB.encryptor()
	encrypted_ECB = encryptor_ECB.update(to_encrypt_bytes) + encryptor_ECB.finalize()


################################### CBC mode #########################
	iv = randBytes(16)
	cipher_CBC = Cipher(algorithms.AES(rk), modes.CBC(iv), backend=default_backend())
	encryptor_CBC = cipher_CBC.encryptor()
	encrypted_CBC = encryptor_CBC.update(to_encrypt_bytes) + encryptor_CBC.finalize()

	print("ECB encrypted: ", encrypted_ECB)
	print("CBC encrypted: ", encrypted_CBC)

############################## Choose encryption method ##############################
	if random.randint(0,1) == 0:
		print("ECB was the answer")
		return encrypted_ECB
	else:
		print("CBC was the answer")
		return encrypted_CBC


################################### Oracle ##############################
##### Observation:
##### In order for the oracle to work, the plaintext must be sufficient in length and it must also have
##### repeated values
##### Code below was taken from challenge 8
def oracle(encrypted_data):
	encrypted = []
	hex_encrypt = encrypted_data.hex()
	d = {}
	print(hex_encrypt)
	for count, text in enumerate(hex_encrypt):
		if hex_encrypt[count:count+16] not in d:
			d[ hex_encrypt[count:count+16] ] = 1
		else:
			print('Found a repeat in the ciphertext: ', text, ' in position ', count) 
			print('Oracle says...ECB mode')
			return
	# print(d)
	print('Oracle says...CBC mode')

def main():

	### Testing ###
	rk = randBytes(16)
	print("random key: ", rk, "of length", len(rk))

##### Observation:
##### If we specify the testing input as somethink like "a secret message" repeated too few number of times,
##### the oracle will not be able to crack the encoding method
##### Specifically, the encoded text needs to be at least 4 block sizes long
	# encrypted_data = encryptData('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
	encrypted_data = encryptData('a secret message' * 4)
	prediction = oracle(encrypted_data)


if __name__ == '__main__':
	main()