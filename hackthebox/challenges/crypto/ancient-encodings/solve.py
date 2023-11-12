from Crypto.Util.number import long_to_bytes
from base64 import b64decode
print(b64decode(long_to_bytes(int('53465243657a51784d56383361444e664d32356a4d475178626a6c664e44497a5832677a4d6a4e664e7a42664e5463306558303d', 16)).decode()))
# HTB{411_7h3_3nc0d1n9_423_h323_70_574y}