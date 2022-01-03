import requests
import json
from Crypto.Util.number import bytes_to_long, long_to_bytes



def main():
	URL = 'http://aes.cryptohack.org/flipping_cookie/'
	CHECK_ADMIN = 'check_admin/'
	GET_COOKIE = 'get_cookie/'

	r = requests.get(URL + GET_COOKIE)
	j = json.loads(r.text)
	cookie = j["cookie"]
	iv = cookie[:32]
	c = cookie[32:64]
	desired_p = b'admin=True;' # the rest can be whatever
	desired_pt = 'admin=True;'
	p = b'admin=False'

	iva = [int(iv[i:i+2], 16) for i in range(0, len(iv), 2)]

	y = []
	for i in range(len(p)):
		y.append(p[i] ^ desired_p[i])


	print(''.join([chr(a ^ b) for a,b in zip(y, p)]))
	assert(''.join([chr(a ^ b) for a,b in zip(y, p)]) == desired_pt)

	iv_to_send = ''
	for i in range(len(y)):
		iv_to_send += hex(y[i] ^ iva[i])[2:].zfill(2)
		# print(hex(y[i] ^ iva[i])[2:].zfill(2))
	
	assert(len(iv_to_send) == len(y) * 2)

	iv_to_send += iv[len(iv_to_send):]
	assert(len(iv_to_send) % 32 == 0)
	print(iv_to_send)

	r = requests.get(URL + CHECK_ADMIN + cookie[32:] + "/" + iv_to_send + "/")
	j = json.loads(r.text)
	print(j)
	print(j["flag"])

	# Flag: crypto{4u7h3n71c4710n_15_3553n714l}



	




if __name__ == '__main__':
	main()