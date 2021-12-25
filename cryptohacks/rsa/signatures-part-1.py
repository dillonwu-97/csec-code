from pwn import *
import json


def signing_server():
	HOST = 'socket.cryptohack.org'
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

	
	


def main():
	signing_server()


if __name__ == '__main__':
	main()