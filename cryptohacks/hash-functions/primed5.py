from pwn import *
from Crypto.PublicKey import RSA
from Crypto.Hash import MD5
from Crypto.Signature import pkcs1_15
from Crypto.Util.number import long_to_bytes, isPrime
import math
import json

HOST = 'socket.cryptohack.org'
PORT = 13392
# data = {}
# payload = json.dumps(data)


# from secrets import N, E, D

FLAG = "crypto{??????????????????}"

N = 55
E = 13
D = 37
key = RSA.construct((N, E, D))
sig_scheme = pkcs1_15.new(key)
print(key)
print(sig_scheme)
# hash = MD5.new(long_to_bytes(7))
# print(sig_scheme.sign(hash))

def send_sign(r, p):
	data = {"option":"sign", "prime":str(p)}
	payload = json.dumps(data)
	r.sendline(payload)
	p = r.recvline()
	return json.loads(p.decode())["signature"]

def send_check(r, p, s, a):
	data = {"option":"check", "prime": str(p), "signature": s, "a": str(a)}
	payload = json.dumps(data)
	r.sendline(payload)
	p = r.recvline()
	print(p)

def main():
	r = remote(HOST, PORT)
	r.recvuntil("prime\n")
	s = send_sign(r, 7)
	send_check(r, 7, s, 6)
	# send(r, 11)


if __name__ == '__main__':
	main()







