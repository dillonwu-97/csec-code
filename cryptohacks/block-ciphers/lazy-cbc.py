import requests
import json

# https://crypto.stackexchange.com/questions/16161/problems-with-using-aes-key-as-iv-in-cbc-mode

URL = 'http://aes.cryptohack.org/lazy_cbc/'
ENCRYPT = 'encrypt/'
RECEIVE = 'receive/'
GET_FLAG = 'get_flag/'


c = '64' * 32
c0 = c[:32]
c1 = c[32:]

r = requests.get(URL + RECEIVE + c + "/")
j = json.loads(r.text)
pt = j['error'].split(": ")[1]

p0 = pt[:32]
p1 = pt[32:]

print(c0)
print(p1, len(p1))
cprime = [int(c0[i:i+2], 16) ^ int(p1[i:i+2], 16) for i in range(0,len(p1), 2)]
iv = [int(p0[i:i+2], 16) for i in range(0,len(p0), 2)]
for i in range(len(cprime)):
	iv[i] ^= cprime[i]
iv = ''.join([hex(i)[2:] for i in iv])

r = requests.get(URL + GET_FLAG + iv + "/")
j = json.loads(r.text)
print(bytes.fromhex(j['plaintext']))

# Flag: crypto{50m3_p30pl3_d0n7_7h1nk_IV_15_1mp0r74n7_?}




