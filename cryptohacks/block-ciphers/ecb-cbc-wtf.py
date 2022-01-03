import requests
import json
from Crypto.Util.number import bytes_to_long, long_to_bytes

def hexi(a,b):
	return ''.join([chr(x ^ y) for (x,y) in zip(a,b)])

def main():
	URL = 'http://aes.cryptohack.org/ecbcbcwtf/'
	DEC = 'decrypt/'
	FLAG = 'encrypt_flag/'

	r = requests.get(URL + FLAG)
	j = json.loads(r.text)
	c = j['ciphertext']
	chunks = []
	iv = c[:32]
	for i in range(32,len(c),32):
		chunks.append(c[i:i+32])

	p_chunks = []
	for i in chunks:
		r = requests.get(URL + DEC + i + "/")
		j = json.loads(r.text)
		p_chunks.append(j['plaintext'])

	prev = bytes.fromhex(iv)
	ret = ''
	for i in range(len(p_chunks)):
		temp = bytes.fromhex(p_chunks[i])
		print("val is ", hexi(prev, temp))
		ret += hexi(prev, temp)
		prev = bytes.fromhex(chunks[i])
	print(ret)
	# Flag: crypto{3cb_5uck5_4v01d_17_!!!!!}




if __name__ == '__main__':
	main()