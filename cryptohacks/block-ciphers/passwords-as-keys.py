import requests
import json
from Crypto.Cipher import AES
import hashlib

def decrypt(ciphertext, key):
    ciphertext = bytes.fromhex(ciphertext)
    # key = bytes.fromhex(password_hash)

    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.decrypt(ciphertext)


def main():
	r = requests.get('http://aes.cryptohack.org/passwords_as_keys/encrypt_flag')
	c = json.loads(r.text)
	ciphertext = c["ciphertext"]

	with open('/Users/Kvothe/Downloads/words.txt', 'r') as f:
		words = [w.strip() for w in f.readlines()]
	
	for i in range(len(words)):
		print(i)
		KEY = hashlib.md5(words[i].encode()).digest()
		try:
			print(decrypt(ciphertext, KEY).decode('ascii'))
			break
		except:
			continue


if __name__ == '__main__':
	main()