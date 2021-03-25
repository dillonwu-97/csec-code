import base64
from Crypto.Util.number import long_to_bytes
from pwn import *
import json
import codecs
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import gmpy2
from sympy.solvers.diophantine.diophantine import base_solution_linear, diophantine
from sympy import *
from Crypto.PublicKey import RSA
from asn1crypto.x509 import Certificate


def dec(a):
	return bytes.fromhex(hex(a)[2:]).decode("ascii")

def encoding_challenge():
	r = remote('socket.cryptohack.org', 13377)
	for i in range(101):
		l = r.recvline()
		print("Received: ", l)
		j = json.loads(l)
		# print(j)
		if isinstance(j['encoded'], list):
			to_send = codecs.decode(bytes(j['encoded']),j['type'])
		elif j['type'] == 'hex':
			to_send = codecs.decode(j['encoded'], j['type']).decode('ascii')
		elif j['type'] == 'base64':
			to_send = base64.b64decode(j['encoded']).decode('ascii')
		elif j['type'] == 'bigint': 
			to_send = long_to_bytes(int(j['encoded'][2:], 16)).decode('ascii')
		else: 
			to_send = codecs.decode(j['encoded'], j['type'])
		# print(to_send)
		to_send = "{\"decoded\": " + json.dumps(to_send) + "}"
		print("Sending ", to_send)
		r.sendline(to_send)
		# temp = ''.join([chr(char) for char in j['encoded']])
		# print(temp)
		

def remove_line(s):
    # returns the header line, and the rest of the file
    print(type(s))
    return s[:s.index(b'\n') + 1], s[s.index(b'\n')+1:]

def parse_header_png(data):

    header = b''

    for i in range(2):
        header_i, data = remove_line(data)
        header += header_i

    return header, data

def byte_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

def lemur_xor():

	lemur = Image.open('/Users/Kvothe/Downloads/lemur_ed66878c338e662d3473f0d98eedbd0d.png')
	flag = Image.open('/Users/Kvothe/Downloads/flag_7ae18c704272532658c10b5faad06d74.png')	

	lemur_pix = np.array(lemur)
	flag_pix = np.array(flag)
	lemur_flag = np.bitwise_xor(lemur_pix, flag_pix)
	plt.imsave('/Users/Kvothe/Downloads/lemur_flag.png', lemur_flag.astype(np.uint8))

def main():

	### Solutions: Encoding
	# 1
	# a = [99, 114, 121, 112, 116, 111, 123, 65, 83, 67, 73, 73, 95, 112, 114, 49, 110, 116, 52, 98, 108, 51, 125]
	# sol_1 = "".join([chr(i) for i in a])
	# print(sol_1)

	# 2
	# b = '63727970746f7b596f755f77696c6c5f62655f776f726b696e675f776974685f6865785f737472696e67735f615f6c6f747d'
	# print(bytes.fromhex(b).decode('ascii'))

	# 3
	# c = '72bca9b68fc16ac7beeb8f849dca1d8a783e8acf9679bf9269f7bf'
	# print(base64.b64encode(bytes.fromhex(c)).decode('ascii'))

	# 4
	# d = 11515195063862318899931685488813747395775516287289682636499965282714637259206269
	# print(long_to_bytes(d).decode('ascii'))

	# encoding_challenge()

	### Solutions: XOR
	# # 1
	# a = "label"
	# b = 13
	# c = ""
	# for i in a:
	# 	c += chr(b ^ ord(i))
	# print("crypto{" + c + "}")

	# #2 
	# KEY1 = 0xa6c8b6733c9b22de7bc0253266a3867df55acde8635e19c73313
	# KEY2KEY1 = 0x37dcb292030faa90d07eec17e3b1c6d8daf94c35d4c9191a5e1e
	# KEY2KEY3 = 0xc1545756687e7573db23aa1c3452a098b71a7fbf0fddddde5fc1
	# FLAGKEY1KEY3KEY2 = 0x04ee9855208a2cd59091d04767ae47963170d1660df7f56f5faf
	# res = FLAGKEY1KEY3KEY2 ^ KEY2KEY3 ^ KEY1
	# print(dec(res))

	# #3 
	# a = hex(0x73626960647f6b206821204f21254f7d694f7624662065622127234f726927756d)
	# for i in range(128):	
	# 	current = ''
	# 	for j in range(2, len(a), 2):
	# 		current += chr(int(a[j:j+2], 16) ^ i)
	# 	if current.find("crypto") != -1:
	# 		print(current)
	# 		break
		
	# #4
	# a = '0' + hex(0x0e0b213f26041e480b26217f27342e175d0e070a3c5b103e2526217f27342e175d0e077e263451150104)[2:]
	# start = "crypto{1"
	# keys = []
	# for i in range(len(start)):
	# 	# print(a[2*i:2*i + 2], start[i])
	# 	keys.append( ord(start[i]) ^ int( a[2*i:2*i + 2], 16) )
	# ret = ""
	# # print(keys)
	# for i in range(0, len(a),2):
	# 	ret += chr( keys[(i//2)%len(keys)] ^ int( a[i: i + 2], 16 ))
	# print(ret)

	#5
	# lemur_xor()


	# # Math
	# # 1
	# a = 66528
	# b = 52920
	# print(gmpy2.gcd(a, b))

	# # 2
	# p = 26513
	# q = 32321
	# res = base_solution_linear(1,p,q)
	# # x, y = symbols("x, y")
	# # print(diophantine(p*x + q*y - 1))
	# print("crypto{" + str(res[0]) + "," + str(res[1]) + "}")

	# # 3
	# print(8146798528947 %17)

	# # 4
	# print(pow(273246787654,65536,65537))

	# # 5
	# print(gmpy2.invert(3, 13))

	# Data Formats
	# https://www.cryptologie.net/article/260/asn1-vs-der-vs-pem-vs-x509-vs-pkcs7-vs/
	# private key:
	# 	-----BEGIN RSA PRIVATE KEY-----
	# MIIEowIBAAKCAQEAzvKDt+EO+A6oE1LItSunkWJ8vN6Tgcu8Ck077joGDfG2NtxD
	# 4vyQxGTQngr6jEKJuVz2MIwDcdXtFLIF+ISX9HfALQ3yiedNS80n/TR1BNcJSlzI
	# uqLmFxddmjmfUvHFuFLvxgXRga3mg3r7olTW+1fxOS0ZVeDJqFCaORRvoAYOgLgu
	# d2/E0aaaJi9cN7CjmdJ7Q3m6ryGuCwqEvZ1KgVWWa7fKcFopnl/fcsSecwbDV5hW
	# fmvxiAUJy1mNSPwkf5YhGQ+83g9N588RpLLMXmgt6KimtiWnJsqtDPRlY4Bjxdpu
	# V3QyUdo2ymqnquZnE/vlU/hn6/s8+ctdTqfSCwIDAQABAoIBAHw7HVNPKZtDwSYI
	# djA8CpW+F7+Rpd8vHKzafHWgI25PgeEhDSfAEm+zTYDyekGk1+SMp8Ww54h4sZ/Q
	# 1sC/aDD7ikQBsW2TitVMTQs1aGIFbLBVTrKrg5CtGCWzHa+/L8BdGU84wvIkINMh
	# CtoCMCQmQMrgBeuFy8jcyhgl6nSW2bFwxcv+NU/hmmMQK4LzjV18JRc1IIuDpUJA
	# kn+JmEjBal/nDOlQ2v97+fS3G1mBAaUgSM0wwWy5lDMLEFktLJXU0OV59Sh/90qI
	# Jo0DiWmMj3ua6BPzkkaJPQJmHPCNnLzsn3Is920OlvHhdzfins6GdnZ8tuHfDb0t
	# cx7YSLECgYEA7ftHFeupO8TCy+cSyAgQJ8yGqNKNLHjJcg5t5vaAMeDjT/pe7w/R
	# 0IWuScCoADiL9+6YqUp34RgeYDkks7O7nc6XuABi8oMMjxGYPfrdVfH5zlNimS4U
	# wl93bvfazutxnhz58vYvS6bQA95NQn7rWk2YFWRPzhJVkxvfK6N/x6cCgYEA3p21
	# w10lYvHNNiI0KBjHvroDMyB+39vD8mSObRQQuJFJdKWuMq+o5OrkC0KtpYZ+Gw4z
	# L9DQosip3hrb7b2B+bq0yP7Izj5mAVXizQTGkluT/YivvgXcxVKoNuNTqTEgmyOh
	# Pn6w+PqRnESsSFzjfWrahTCrVomcZmnUTFh0rv0CgYBETN68+tKqNbFWhe4M/Mtu
	# MLPhFfSwc8YU9vEx3UMzjYCPvqKqZ9bmyscXobRVw+Tf9llYFOhM8Pge06el74qE
	# IvvGMk4zncrn8LvJ5grKFNWGEsZ0ghYxJucHMRlaU5ZbM6PEyEUQqEKBKbbww65W
	# T3i7gvuof/iRbOljA9yzdwKBgQDT9Pc+Fu7k4XNRCon8b3OnnjYztMn4XKeZn7KY
	# GtW81eBJpwJQEj5OD3OnYQoyovZozkFgUoKDq2lJJuul1ZzuaJ1/Dk+lR3YZ6Wtz
	# ZwumCHnEmSMzWyOT4Rp2gEWEv1jbPbZl6XyY4wJG9n/OulqDbHy4+dj5ITb/r93J
	# /yLCBQKBgHa8XYMLzH63Ieh69VZF/7jO3d3lZ4LlMEYT0BF7synfe9q6x7s0ia9b
	# f6/QCkmOxPC868qhOMgSS48L+TMKmQNQSm9b9oy2ILlLA0KDsX5O/Foyiz1scwr7
	# nh6tZ+tVQCRvFviIEGkaXdEiBN4eTbcjfc5md/u9eA5N21Pzgd/G
	# -----END RSA PRIVATE KEY-----

	# d = '7C:3B:1D:53:4F:29:9B:43:C1:26:08:76:30:3C:0A:95:BE:17:BF:91:A5:DF:2F:1C:AC:DA:7C:75:A0:23:6E:4F:81:E1:21:0D:27:C0:12:6F:B3:4D:80:F2:7A:41:A4:D7:E4:8C:A7:C5:B0:E7:88:78:B1:9F:D0:D6:C0:BF:68:30:FB:8A:44:01:B1:6D:93:8A:D5:4C:4D:0B:35:68:62:05:6C:B0:55:4E:B2:AB:83:90:AD:18:25:B3:1D:AF:BF:2F:C0:5D:19:4F:38:C2:F2:24:20:D3:21:0A:DA:02:30:24:26:40:CA:E0:05:EB:85:CB:C8:DC:CA:18:25:EA:74:96:D9:B1:70:C5:CB:FE:35:4F:E1:9A:63:10:2B:82:F3:8D:5D:7C:25:17:35:20:8B:83:A5:42:40:92:7F:89:98:48:C1:6A:5F:E7:0C:E9:50:DA:FF:7B:F9:F4:B7:1B:59:81:01:A5:20:48:CD:30:C1:6C:B9:94:33:0B:10:59:2D:2C:95:D4:D0:E5:79:F5:28:7F:F7:4A:88:26:8D:03:89:69:8C:8F:7B:9A:E8:13:F3:92:46:89:3D:02:66:1C:F0:8D:9C:BC:EC:9F:72:2C:F7:6D:0E:96:F1:E1:77:37:E2:9E:CE:86:76:76:7C:B6:E1:DF:0D:BD:2D:73:1E:D8:48:B1'
	# d = int(d.replace(":", "").lower(),16)
	# print(d)

	# # 1
	# f = open('/Users/Kvothe/Downloads/privacy_enhanced_mail_1f696c053d76a78c2c531bb013a92d4a.pem','r')
	# key = RSA.importKey(f.read())
	# print(key.d)

	# # 2
	# f = open('/Users/Kvothe/Downloads/2048b-rsa-example-cert_3220bd92e30015fe4fbeb84a755e7ca5.der', 'rb')
	# cert = Certificate.load(f.read())

	# n = cert.public_key.native["public_key"]["modulus"]

	# print(n)

	# # 3
	with open('/Users/Kvothe/Downloads/transparency_afff0345c6f99bf80eab5895458d8eab.pem') as f:
		cert = f.read()

	key = RSA.importKey(cert)
	print(hex(key.n))


	

if __name__ == '__main__':
	main()

