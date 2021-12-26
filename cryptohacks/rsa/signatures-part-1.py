from pwn import *
import json
from pkcs1 import emsa_pkcs1_v15
from Crypto.Util.number import bytes_to_long

HOST = 'socket.cryptohack.org'
def signing_server():
	
	PORT = 13374
	r = remote(HOST, PORT)
	r.recvuntil("sign.\n")
	data1 = {'option': 'get_secret'}
	payload1 = json.dumps(data1)
	r.sendline(payload1)
	p = r.recvline()
	secret = json.loads(p)['secret'][2:]
	print("Secret: ", secret)
	data2 = {'option': 'sign', 'msg': secret}
	payload2 = json.dumps(data2)
	r.sendline(payload2)
	p = r.recvline()
	sig = json.loads(p)['signature']
	sig = bytes.fromhex(sig[2:])
	print(sig)
	# Flag: crypto{d0n7_516n_ju57_4ny7h1n6}

def lets_decrypt():

	# I can control e and n in this code
	PORT = 13391
	r = remote(HOST, PORT)
	r.recvuntil("domain.\n")

	data1 = {"option": "get_signature"}
	payload1 = json.dumps(data1)
	r.sendline(payload1)
	p = json.loads(r.recvline())
	N = int(p['N'][2:],16)
	e = int(p['e'][2:],16)
	signature = int(p['signature'],16)
	# print(N)
	# print(e)
	# print(signature)

	msg = "I am Mallory. I own CryptoHack.org"
	digest = emsa_pkcs1_v15.encode(msg.encode(), 256)
	dnum = bytes_to_long(digest)
	# You can control e and N so 
	# formula: digest = Signature ^ power %  (Signature ^ power - (Signature ^ power - digest))
	p = 1
	while (signature ** p < dnum):
		p += 1
	N = hex(signature - dnum)[2:].zfill(2)
	e = hex(1)[2:].zfill(2)
	
	data1 = {"option": "verify", "msg": msg, "N": N, "e": e}
	payload2 = json.dumps(data1)
	calculated_digest = pow(signature, int(e, 16), int(N,16))
	assert(signature > dnum)
	assert(calculated_digest == dnum)
	print(calculated_digest)
	print(dnum)
	r.sendline(payload2)
	p = r.recvline()
	print(p)
	# Flag: crypto{dupl1c4t3_s1gn4tur3_k3y_s3l3ct10n}

def main():
	# signing_server()
	lets_decrypt()


if __name__ == '__main__':
	main()