import requests
import json
from Crypto.Util.number import long_to_bytes

# goal is just to extract the IV
URL = 'http://aes.cryptohack.org/triple_des/'
ENCRYPT_FLAG = 'encrypt_flag/'
ENCRYPT = 'encrypt/'
# https://www.cs.purdue.edu/homes/ninghui/courses/Fall05/lectures/355_Fall05_lect17.pdf
# https://en.wikipedia.org/wiki/Weak_key
# key = 'f' * 24 + '0' * 24
# key = '0' * 24 + 'f' * 24
# 0000000 0000000
# 0000000 FFFFFFF
# FFFFFFF 0000000
# FFFFFFF FFFFFFF
# key = '0' * 21 + '1' * 14 + '0' * 7 + '1' * 14
key = 'E1E1E1E1F0F0F0F01E1E1E1E0F0F0F0F'
key = '0000000000000000E1E1E1E1F0F0F0F0'

# Weak key attack essentially

key1 = b''
r = requests.get(URL + ENCRYPT_FLAG + key + "/")
j = json.loads(r.text)
print(j)
ct = j["ciphertext"]
# long_to_bytes(int(j["ciphertext"],16)))

r = requests.get(URL + ENCRYPT + key + "/" + ct + "/")
j = json.loads(r.text)
pt = j["ciphertext"]
print(pt)
print(long_to_bytes(int(j["ciphertext"],16)))


# Flag: