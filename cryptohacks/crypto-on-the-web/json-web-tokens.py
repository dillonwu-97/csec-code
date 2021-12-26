import jwt
import base64
import requests
import json
from Crypto.PublicKey import RSA

def get_s(token):
	t = token.split('.')
	ret = []
	for i in t:
		d = base64.b64decode(i + '=' * (4 - len(token) % 4))
		ret.append(d)
	return ret

def token_appreciation():
	token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmbGFnIjoiY3J5cHRve2p3dF9jb250ZW50c19jYW5fYmVfZWFzaWx5X3ZpZXdlZH0iLCJ1c2VyIjoiQ3J5cHRvIE1jSGFjayIsImV4cCI6MjAwNTAzMzQ5M30.shKSmZfgGVvd2OSB2CGezzJ3N6WAULo3w9zCl_T47KQ'
	t = token.split('.')
	for i in t:
		d = base64.b64decode(i + '=' * (4 - len(token) % 4))
		print(d)
	# Flag: crypto{jwt_contents_can_be_easily_viewed}

def no_way_jose():
	url = 'http://web.cryptohack.org/no-way-jose/'
	create_session = 'create_session/user/'
	r = requests.get(url + create_session)
	j = json.loads(r.text)
	session = j['session']
	s_split = get_s(session)
	print(s_split)
	p1 = json.loads(s_split[0])
	p2 = json.loads(s_split[1])

	# Constructing payload
	print(p2)
	p1["alg"] = "none"
	p2["admin"] = True
	print(p2)

	t1 = base64.b64encode(json.dumps(p1).replace('-','+').replace('_','/').encode()).decode()
	t2 = base64.b64encode(json.dumps(p2).replace('-','+').replace('_','/').encode()).decode()

	print(t1, t2, s_split[2])
	payload = t1 + '.' + t2 + '.' + j['session'].split('.')[2]
	print(payload)
	# token_b64 = token.replace('-', '+').replace('_', '/') # JWTs use base64url encoding
	authorize = 'authorise/'
	r = requests.get(url + authorize + '/' + payload)
	j = json.loads(r.text)
	print(j)
	# Flag: crypto{The_Cryptographic_Doom_Principle}

def jwt_secrets():
	KEY = "secret"
	url = 'http://web.cryptohack.org/jwt-secrets/'
	create_session = 'create_session/user/'
	authorize = 'authorise/'
	token = jwt.encode({'username': "user", 'admin':True},KEY, algorithm='HS256')
	r = requests.get(url + authorize + token + '/')
	j = json.loads(r.text)
	print(j)
	# Flag: crypto{jwt_secret_keys_must_be_protected}
	
	return None

def rsa_or_hmac():
	# pip install pyjwt==1.5.0
	url = 'http://web.cryptohack.org/rsa-or-hmac/'
	get_pk = 'get_pubkey/'
	r = requests.get(url + get_pk)
	r = json.loads(r.text)
	pk = r['pubkey']
	# pk = r ['pubkey'].split("-----")[2]
	# keyDER = base64.b64decode(pk)
	# keyPub = RSA.importKey(keyDER)
	token = jwt.encode({'username': 'user', 'admin':True}, pk, algorithm='HS256')
	authorize = 'authorise/'
	print(token.decode())
	full_url = url + authorize + token.decode() + '/'
	print(full_url)
	r = requests.get(full_url)
	print(r)
	j = json.loads(r.text)
	print(j)
	# Flag: crypto{Doom_Principle_Strikes_Again}


def main():
	# token_appreciation()

	# Jwt sessions puzzle
	# Flag: Authorization

	# no_way_jose()

	# jwt_secrets()

	rsa_or_hmac()

if __name__ == '__main__':
	main()

