'''
The Base64-encoded content in this file has been encrypted via AES-128 in ECB mode under the key

"YELLOW SUBMARINE".
(case-sensitive, without the quotes; exactly 16 characters; I like "YELLOW SUBMARINE" because it's exactly 16 bytes long, and now you do too).

Decrypt it. You know the key, after all.

Easiest way: use OpenSSL::Cipher and give it AES-128-ECB as the cipher.
'''

import base64
import binascii
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

from Crypto.Cipher import AES

def main():
	filetxt = ''
	with open('file.txt', 'r') as f:
		# for i in f:
		# 	filetxt+= i.strip('\n').strip('\r')
		filetxt = f.read()

	# print(filetxt)
	############################## Using cryptography library ###################################
	filetxt = bytes.fromhex(base64.b64decode(filetxt).hex())
	key = b'YELLOW SUBMARINE'
	hexkey = binascii.hexlify(key)
	# print(hexkey)

	cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
	encryptor = cipher.encryptor()
	### Test ###
	ct = encryptor.update(b"a secret message") + encryptor.finalize()
	# print(ct)
	############
	decryptor = cipher.decryptor()
	result = decryptor.update(filetxt) + decryptor.finalize()
	print(result.decode())
	###############################################################################################


	############################## Using Crypto.cipher library ###################################
	cipher = AES.new(key, AES.MODE_ECB)
	print(cipher.decrypt(filetxt).decode())



if __name__ == '__main__':
	main()