import gmpy2
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib

# intercepted from alice
# contains p, g, A
alice = {"p": "0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff", "g": "0x02", "A": "0xd6dd08a0d9203aff5865fd42d71da85bfa2701efa088278576ede83ceba66486f6a10100533ce4f2b0b0c5e36f69ca4f1ae8cdfb7e69356c00fbf4644168a81abd8be03ba2cb695a0f2de29439af3ab6e86e628bb9737a40d7d98bdbe75b6c15855da61d517da54e87eb08de9f54e6421c793f3b4f9698786ccc55edecc99bbdd2381a4fe84f5358c267ea3ed98718aaaf37d602567b0e1835637e8464275efe2162cbba65179934a5087d62a69b6f252a63cd336cada964fff2905b34710f97"}
p = int(alice["p"][2:], 16)
g = int(alice["g"][2:], 16)
A = int(alice["A"][2:], 16)
# coming up with my own keys
private_key = 3
public_key = pow(g, private_key, p)
send_to_alice = "{\"B\": \"" + hex(public_key) + "\"}"
print(send_to_alice)
shared_key = pow(A, private_key, p)
alice_intercept={"iv": "7e571ec7b33a79a1981c886bdf1a9121", "encrypted_flag": "d3f75638ee1352101e6c709469b458dd778461cbbfc7f6b55674a3cf4ebbef49"}
# inv_shared = gmpy2.invert(shared_key, p)


def is_pkcs7_padded(message):
	padding = message[-message[-1]:]
	return all(padding[i] == len(padding) for i in range(0, len(padding)))


def decrypt_flag(shared_secret: int, iv: str, ciphertext: str):
	# Derive AES key from shared secret
	sha1 = hashlib.sha1()
	sha1.update(str(shared_secret).encode('ascii'))
	key = sha1.digest()[:16]
	# Decrypt flag
	ciphertext = bytes.fromhex(ciphertext)
	iv = bytes.fromhex(iv)
	cipher = AES.new(key, AES.MODE_CBC, iv)
	plaintext = cipher.decrypt(ciphertext)

	if is_pkcs7_padded(plaintext):
		return unpad(plaintext, 16).decode('ascii')
	else:
		print(plaintext)
		return plaintext.decode('ascii')


# print(hex(shared_key)[2:])
shared_secret = shared_key
iv = alice_intercept["iv"]
ciphertext = alice_intercept["encrypted_flag"]

print(decrypt_flag(shared_secret, iv, ciphertext))


# alice_payload = "{" + "\"p\": \"" + alice["p"] + "\", \"g\": \"0x02\", \"A\": \"" + str(hex(shared_key)) + "\"}"
# print(alice_payload)