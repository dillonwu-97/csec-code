import binascii
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def main(): 

	with open('file.txt', 'r') as f:
		file = f.read()

############################## setup ##############################
	key = 'YELLOW SUBMARINE'
	bytekey = b'YELLOW SUBMARINE'
	hexkey = binascii.hexlify(str.encode(key))

	test = 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industrys standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.'
	test_hex = binascii.hexlify(str.encode(test))
	# padding
	if len(test) % len(key) != 0:
		test += " " * (len(key) - len(test) % len(key))

	iv = '0' * len(key)
	iv_byte = b'0' * len(key)

	file = bytes.fromhex(base64.b64decode(file).hex())
######################################################################

################################ encryption ##############################
##### Lesson: Conversions between string -> bytes can result in bugs; it is better to convert from
##### integers -> bytes and back
	cipher = Cipher(algorithms.AES(bytekey), modes.ECB(), backend=default_backend())
	encryptor = cipher.encryptor()
	prev = iv
	prev_ord = [ord(i) for i in prev]
	cipher_text = b''
	for i in range(0,len(test), len(key)):
		plain_ord = [ord(test[i]) for i in range(i, i+16)]
		cipher_ord = [prev_ord[i] ^ plain_ord[i] for i in range(16)]
		to_encrypt = b''
		for i in cipher_ord:
			to_encrypt += bytes([i])
			# print(bytes([i]), i)
		cipher_block = encryptor.update(to_encrypt)
		prev_ord = [cipher_block[i] for i in range(len(cipher_block))]
		cipher_text += cipher_block
	cipher_text += encryptor.finalize()
	print("#################### Encryption complete ####################")
	print(cipher_text)
	# print(binascii.unhexlify(cipher_text))

	decryption_cipher = Cipher(algorithms.AES(bytekey), modes.CBC(iv_byte), backend=default_backend())
	decryptor = decryption_cipher.decryptor()
	result = decryptor.update(cipher_text) + decryptor.finalize() # <-- returns xor values...
	print("############### Checking decryption ####################")
	print(result) 

	print("#################### Decrypting file #########################")
	decryption_cipher = Cipher(algorithms.AES(bytekey), modes.ECB(), backend=default_backend())
	decryptor = decryption_cipher.decryptor()
	plain_final = ""
	for i in range(len(file)-16, 15, -16):
		# cipher_text = [file[i] for i in range(i, i+16)] # get cipher text
		cipher_bytes = file[i:i+16]
		xor_block = decryptor.update(cipher_bytes)
		xor_text = [xor_block[i] for i in range(len(xor_block))]
		prev_cipher_text = [file[i] for i in range(i-16, i)]
		# print(xor_text, prev_cipher_text)
		plain_text = "".join([chr(xor_text[i] ^ prev_cipher_text[i]) for i in range(16)])
		plain_final = plain_text + plain_final
	# start of block
	cipher_bytes = file[0:16]
	xor_block = decryptor.update(cipher_bytes)
	xor_text = [xor_block[i] for i in range(len(xor_block))]
	prev_cipher_text = [0] * 16 # iv value
	plain_text = "".join([chr(xor_text[i] ^ prev_cipher_text[i]) for i in range(16)])
	plain_final = plain_text + plain_final


	print(plain_final)
	
	
	
if __name__ == '__main__':
	main()