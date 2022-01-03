import json
from pwn import *
import requests

# https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Output_feedback_(OFB)
# According to the wiki page, OFB mode encryption and decryption are exactly the same
def main():
	URL = 'http://aes.cryptohack.org/symmetry/'
	ENC = 'encrypt/'
	FLAG = 'encrypt_flag/'

	r = requests.get(URL + FLAG)
	j = json.loads(r.text)
	out = j['ciphertext']
	iv = out[:32]
	c = out[32:]
	print(iv, c)

	payload = URL + ENC + c + "/" + iv + "/"
	print(payload)
	r = requests.get(payload)
	j = json.loads(r.text)

	print(j)
	ret = j['ciphertext']
	print(bytes.fromhex(ret))

	# Flag: crypto{0fb_15_5ymm37r1c4l_!!!11!}

if __name__ == '__main__':
	main()