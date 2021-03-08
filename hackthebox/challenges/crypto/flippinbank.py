import binascii
from Crypto.Util.Padding import pad,unpad
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
from Crypto.Random import get_random_bytes
from binascii import unhexlify


def encrypt_data(data):
	padded = pad(data.encode(),16,style='pkcs7')
	print('inside encrypted"')
	print(data, padded)
	print(len(data), len(padded))
	cipher = AES.new(key, AES.MODE_CBC,iv)
	enc = cipher.encrypt(padded)
	return enc.hex()

def decrypt_data(encryptedParams):
	cipher = AES.new(key, AES.MODE_CBC,iv)
	paddedParams = cipher.decrypt( unhexlify(encryptedParams))
	print(paddedParams)
	if b'admin&password=g0ld3n_b0y' in unpad(paddedParams,16,style='pkcs7'):
		return 1
	else:
		return 0

if __name__ == '__main__':
	data = 'logged_username=bdmin&password=g0ld3n_b0yaaaaaa'
	payload = 'logged_username=admin&password=g0ld3n_b0yaaaaaa'
	ciphertext = 'aa49b0add22457ceb21b45528779851507619d2d2e0d6f9da2f5ee950a14753069a497f1b197e15c0ec963ef0c95d155'
	ciphersplit = []
	for i in range(0,len(ciphertext), 32):
		if (i + 32 > len(ciphertext)):
			ciphersplit.append(ciphertext[i:])
		else:
			ciphersplit.append(ciphertext[i:i+32])
	print(ciphersplit)
	
	print('logged_username=bdmin&password=g0ld3n_b0y' + 'a' * (16 * 3 - 41))

	key = b'a' * 16
	iv = b'a' * 16
	a = encrypt_data(data)
	b = encrypt_data(payload)
	print(a)
	print(b)

	test = b
	test = 'f0' + test[2:]
	print(decrypt_data(test))
	decrypt_data(b)




# The below code doesn't work because the encryption method is not a simple xor; it is AES
# need to do cbc bitflipping attack instead
# if __name__ == '__main__':
# 	print(len('aa49b0add22457ceb21b455287798515'))
# 	print(len('logged_username='))

# 	# ciphertext is padded
# 	ciphertext = 'aa49b0add22457ceb21b45528779851507619d2d2e0d6f9da2f5ee950a147530a67b457d31e379a86ae743de0db8a1e3'
# 	plaintext = binascii.hexlify(str.encode('logged_username=bdmin&password=g0ld3n_b0y')).decode("utf-8") + "07" * 14
# 	payload = binascii.hexlify(str.encode('logged_username=admin&password=g0ld3n_b0y')).decode("utf-8") + "07" * 14

# 	# print(len(ciphertext), len(plaintext))
# 	ciphersplit = []
# 	plainsplit = []
# 	payloadsplit = []
# 	for i in range(0,len(ciphertext), 32):
# 		if (i + 32 > len(ciphertext)):
# 			ciphersplit.append(ciphertext[i:])
# 			plainsplit.append(plaintext[i:])
# 			payloadsplit.append(payload[i:])
# 		else:
# 			ciphersplit.append(ciphertext[i:i+32])
# 			plainsplit.append(plaintext[i:i+32])
# 			payloadsplit.append(payload[i:i+32])
# 	print(ciphersplit)
# 	print(plainsplit)
# 	print(payloadsplit)

# 	payloadsplit = plainsplit
# 	# # print(user1_split[0], binascii.hexlify(str.encode(plain_split[1])))
# 	key = []
# 	for i in range(0,32,2):
# 		key.append(int(ciphersplit[0][i:i+2],16) ^ int(plainsplit[1][i:i+2],16) ^ int(ciphersplit[1][i:i+2], 16))
# 		# print(int(ciphersplit[0][i:i+2],16), int(plainsplit[1][i:i+2],16), int(payloadsplit[1][i:i+2], 16))
# 	print(key)

# 	ret = ciphersplit[0]
# 	temp = ''
# 	for i in range(0,32,2):
# 		# previous ciphertext xor plaintext xor key = new ciphertext
# 		# print(ciphersplit[0][i], payloadsplit[1][i], key[i])
# 		# temp += chr(int(ciphersplit[0][i:i+2],16) ^ int(plainsplit[1][i:i+2],16) ^ key[i//2])
# 		cur = hex(int(ciphersplit[0][i:i+2],16) ^ int(payloadsplit[1][i:i+2],16) ^ key[i//2])[2:].zfill(2)
# 		print(cur)
# 		temp += cur
# 	print(temp)
# 	ret += temp



# 	temp2 = ''
# 	for i in range(0, len(payloadsplit[-1]),2):
# 		print(int(temp[i:i+2], 16), int(payloadsplit[-1][i:i+2], 16), key[i//2])
# 		cur = hex(int(temp[i:i+2], 16) ^ int(payloadsplit[-1][i:i+2], 16) ^ key[i//2]) [2:].zfill(2)
# 		temp2 += cur
	
# 	ret += temp2
# 	print(ret)




