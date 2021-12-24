from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import json
from pwn import *
import hashpumpy

HOST = 'socket.cryptohack.org'
PORT = 13388


### Sandbox ###

def bxor(a, b):
	return bytes(x ^ y for x, y in zip(a, b))

def hash(data):
	data = pad(data, 16)
	out = b"\x00" * 16
	for i in range(0, len(data), 16):
		blk = data[i:i+16]
		# print("blk is ", blk)
		# print("out before is ", out)
		out = bxor(AES.new(blk, AES.MODE_ECB).encrypt(out), out)
		# assert(blk == out)
		print("-" * 100)
		print(blk, out)
		# print("out after is ", out)
	return out
KEY = b'abcd' * 4
sig = hash(KEY + b"hello")
print(sig.hex())

data = pad(b"admin=True", 16)
print(data)
new_hash = bxor(AES.new(data, AES.MODE_ECB).encrypt(sig), sig)
print(bytes.fromhex(new_hash.hex()))
assert (new_hash == bytes.fromhex(new_hash.hex()))


# Not this
# new_hash, msg = hashpumpy.hashpump(sig.hex(), 'hello', 'admin=True', 16)
# print("New hash is: ", new_hash)
# print("Message: ", msg)
# print(hash(KEY + msg).hex())

##############

data1 = {"option": "sign", "message": "hello".encode().hex()}
payload1 = json.dumps(data1)
r = remote(HOST, PORT)
r.recvuntil("signatures!\n")
r.sendline(payload1)
sig = r.recvline()
sig = json.loads(sig.decode())['signature']
print("Signature is: ", sig)

data = pad(b"admin=True", 16)
sig = bytes.fromhex(sig)
new_hash = bxor(AES.new(data, AES.MODE_ECB).encrypt(sig), sig).hex()
print("New signature is: ", new_hash)
msg = pad(b"hello", 16) + b"admin=True"
print(msg)

data2 = {"option": "get_flag", "signature":sig, "message":"hello".encode().hex()}
data2 = {"option": "get_flag", "signature": new_hash, "message": msg.hex()}
payload2 = json.dumps(data2)
r.sendline(payload2)
ret = r.recvline()
print(ret)

# Flag: crypto{l3ngth_3xT3nd3r}

