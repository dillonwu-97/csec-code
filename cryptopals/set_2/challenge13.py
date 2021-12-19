'''
ECB cut-and-paste
Write a k=v parsing routine, as if for a structured cookie. The routine should take:

foo=bar&baz=qux&zap=zazzle
... and produce:

{
  foo: 'bar',
  baz: 'qux',
  zap: 'zazzle'
}
(you know, the object; I don't care if you convert it to JSON).

Now write a function that encodes a user profile in that format, given an email address. You should have something like:

profile_for("foo@bar.com")
... and it should produce:

{
  email: 'foo@bar.com',
  uid: 10,
  role: 'user'
}
... encoded as:

email=foo@bar.com&uid=10&role=user
Your "profile_for" function should not allow encoding metacharacters (& and =). Eat them, quote them, whatever you want to do, but don't let people set their email address to "foo@bar.com&role=admin".

Now, two more easy functions. Generate a random AES key, then:

Encrypt the encoded user profile under the key; "provide" that to the "attacker".
Decrypt the encoded user profile and parse it.
Using only the user input to profile_for() (as an oracle to generate "valid" ciphertexts) and the ciphertexts themselves, make a role=admin profile.
'''
import os
import binascii
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import random
from collections import Counter
############################## k=v Parsing #############################################
def kvParse(input):
	kvpair = input.split("&")
	d = {}
	for i in kvpair:
		temp = i.split("=")
		d[temp[0]] = temp[1]
	return d

############################## profile_for function ########################################
def profileFor(email):
	if '&' in email or '=' in email:
		raise ValueError("Bad characters")
	return 'email=' + email + '&uid=10&role=user'

############################## Encrypt ########################################
def encrypt(email, key):
	plaintext = profileFor(email)
	# print(plaintext, len(plaintext))
	plaintext = (plaintext + "A" * (16 - len(plaintext) % 16)).encode() # padding
	cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
	encryptor = cipher.encryptor()
	encrypted = encryptor.update(plaintext) + encryptor.finalize()
	return encrypted

############################## Decrypt ########################################
def decrypt(ciphertext, key):
	cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
	decryptor = cipher.decryptor()
	decrypted = decryptor.update(ciphertext) + decryptor.finalize()
	# print(decrypted.decode('utf-8'))
	# return decrypted.decode('utf-8', errors='ignore')
	return kvParse(decrypted.decode('utf-8'))

############################## Making Valid Admin profile ########################################
# The construct method generates a valid ciphertext using the ciphertext from encrypt() function
# Thoughts / Ideas
# 1
# Use profileFor as an oracle to determine where the '&' character is
# Idea is: encrypt fake email -> send to profileFor -> profileFor decrypts email -> returns an error if email is no good
# -> find where the & value is based on return value
# 2
# What does the final input need to look like? email=hack@mail.com&uid=10&role=admin
# How do I change user to admin? I can construct email=user and email=admin to see which bytes correspond to which
# I have the encrypt function

def construct(key):
	# | x x x x x x x x x x x x x x x x | <== 16 bytes
	# | e m a i l = a b c d e f g h i j |
	# | k l m n o p q r s @ g m a i l . |
	# | c o m & u i d = 1 0 & r o l e = |
	# | a d m i n A A A A A A A A A A A | 

	# Getting the encrypted characters for email
	email = 'a' * 19 + '@gmail.com'
	email_cipher = encrypt(email, key)
	email_block = email_cipher[:48]
	# print(decrypt(email_cipher[:48], key))

	# Getting the encrypted characters for "admin"
	admin = 'abcdefghijadmin' + chr(11)*11
	admin_cipher = encrypt(admin, key)
	admin_block = admin_cipher[16:32]


	final_block = email_block + admin_block
	return final_block


############################## Main ########################################
def main():
	# kvTest = 'foo=bar&baz=qux&zap=zazzle'
	# kvOut = kvParse(kvTest)
	# print(kvOut)

	# profOut = profileFor("foo@bar.com")
	# print(profOut)

	key = os.urandom(16)

	# Testing functions
	print('------------------------- Start Testing ------------------------------')
	ciphertext = encrypt("foo@bar.com", key)
	print(ciphertext, len(ciphertext))
	print(ciphertext[0:3])

	cipherdown = decrypt(ciphertext, key)
	print(cipherdown)

	# End testing
	print('------------------------- End Testing ------------------------------')

	print('------------------------- Solving Problem ------------------------------')

	hacked = construct(key)
	print("And the admin is...", decrypt(hacked, key))

if __name__ == '__main__':
	main()

