import random
import os
import random
from Crypto.Hash import MD5
import base64
from pwn import *
import json


PREFIX = b"CryptoHack Secure Safe"


################################### Scratchwork #############################################
def xor(a, b):
    return a ^ b

magic1 = 2
magic2 = 11

h1 = 3
h2 = 5
for i in range(2, 2**(random.randint(2, 10))):
    # h1 = h2 ^ h1 ^ h2 ^ h2 ^ h2 ^ magic1
    # h2 cancels so just h1 = magic1 ^ h1 

    # h2 = h2 ^ h1 ^ h1 ^ h1 ^ h1 ^ magic2
    # h2 = magic2 ^ h2
    h1 = xor(magic1, xor(h2, xor(xor(h2, xor(h1, h2)), h2)))
    h2 = xor(xor(xor(h1, xor(xor(h2, h1), h1)), h1), magic2)
s = 'CryptoHack Secure Safe'
print(len(s) * 8)
print(h1, h2)
# print(MD5.new(b'CryptoHack Secure Safe').digest().hex())
# print(MD5.new(b'CryptoHack Secure Safe\x').digest().hex())
################################### End Scratchwork #############################################

# These files were extracted from hashclash found here: https://github.com/cr-marcstevens/hashclash
# The command used was ./hashclash/scripts/poc_no.sh prefix
# where prefix is PREFIX value + '123' <-- '123' is essentially needed for padding because of specifications of the tool
f1 = 'Q3J5cHRvSGFjayBTZWN1cmUgU2FmZTEya5cwTmcqxqoXutB8YALU+RrjW9+jh0vV9XBvWRWkeer2IKlhH1PPLVQKOa3V9kM/TWiJIyh2mZ3YjfXxVEX05hCDpMEncLoFknNISJaRbBm4jPELdb3P0Arfc5wldvhHbM0Et4Axf68='
f2 = 'Q3J5cHRvSGFjbCBTZWN1cmUgU2FmZTEya5cwTmcqxqoXutB8YALU+RrjW9+jh0vV9XBvWRWkeer2IKlhH1PPLVQKOa3V9kM/TWeJIyh2mZ3YjfXxVEX05hCDpMEncLoFknNISJaRbBm4jPELdb3P0Arfc5wldvhHbM0Et4Axf68='


base64_bytes1 = f1.encode('ascii')
message_bytes1 = base64.b64decode(base64_bytes1)

base64_bytes2 = f2.encode('ascii')
message_bytes2 = base64.b64decode(base64_bytes2)

assert(message_bytes2 != message_bytes1)

HOST = 'socket.cryptohack.org'
PORT = 13397
r = remote(HOST, PORT)
data1 = {"option": "insert_key", "key": message_bytes1.hex()}
payload1 = json.dumps(data1)
data2 = {'option': "insert_key", "key": message_bytes2.hex()}
payload2 = json.dumps(data2)
data3 = {"option": "unlock"}
payload3 = json.dumps(data3)
r.recvuntil("safe?\n")

r.sendline(payload1)
print(r.recvline())
r.sendline(payload2)
print(r.recvline())
r.sendline(payload3)
ret = r.recvline()
print(ret)

# Flag: crypto{MD5_15_0n_4_c0ll151On_c0uRz3}



# print(MD5.new(f1).digest().hex())
# print(MD5.new(f2).digest().hex())


