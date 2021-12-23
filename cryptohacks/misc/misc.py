import requests
import time
import hashlib
from Crypto.Util.number import long_to_bytes
from pwn import *

def decode(key, flag):
	ret = ''
	for i in range(0,len(flag),2):
		temp = int(flag[i:i+2], 16) ^ int(key[i:i+2], 16)
		ret+=( chr(temp))
	return ret

def gotta_go_fast():
	PORT = 13372
	HOST = 'socket.cryptohack.org'
	payload = '{"option":"get_flag"}'


	r = remote(HOST, PORT)
	r.recvuntil("fast!\n")
	current_time = int(time.time())
	key = long_to_bytes(current_time)
	key = hashlib.sha256(key).digest()
	key = key.hex()
	r.sendline(payload)
	flag = r.recvline()
	flag = flag.decode().split(": \"")[1].split("\"}")[0]
	print(flag)
	print(decode(key, flag))

def main():
	gotta_go_fast()
	
	


if __name__ == '__main__':
	main()