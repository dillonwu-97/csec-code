import requests
import json
import os


def main():
	url = 'http://aes.cryptohack.org/ctrime/encrypt/'
	# payload = os.urandom(32) 
	# r = requests.get(url + payload.hex())
	# j = json.loads(r.text)
	# print(j)
	# txtsize = len(j['ciphertext'])
	# print(txtsize)

	char_list = '0123456789abcdefghijklmnopqrstuvwxyz_\}\{ABCDEFGHIJKLMNOPQRSTUVWXYZ!.?'

	# assume flag is max _ characters long
	flag = 'crypto{CRIME'
	min_size = 10000
	best_char = ''

	# the letter E was skipped for some reason
	for i in range(20):
		min_size = 10000
		print("next iteration")
		payload = os.urandom(len(flag) + 1) 
		r = requests.get(url + payload.hex())
		j = json.loads(r.text)
		txtsize = len(j['ciphertext'])
		print(txtsize)

		for j in char_list:
			payload = (flag + j).encode()
			r = requests.get(url + payload.hex())
			res = json.loads(r.text)
			temp = len(res['ciphertext'])
			print("j and length are ", j, temp)
			if temp < min_size:
				min_size = temp
				best_char = j
		flag += best_char
		print(flag)



if __name__ == '__main__':
	main()


# from Crypto.Cipher import AES
# from Crypto.Util import Counter
# import zlib


# KEY = ?
# FLAG = ?


# @chal.route('/ctrime/encrypt/<plaintext>/')
# def encrypt(plaintext):
#     plaintext = bytes.fromhex(plaintext)

#     iv = int.from_bytes(os.urandom(16), 'big')
#     cipher = AES.new(KEY, AES.MODE_CTR, counter=Counter.new(128, initial_value=iv))
#     encrypted = cipher.encrypt(zlib.compress(plaintext + FLAG.encode()))

#     return {"ciphertext": encrypted.hex()}