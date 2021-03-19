import gmpy2
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib
import math

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
		return plaintext.decode('ascii')

def parameter_injection():
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
	shared_key = pow(A, private_key, p)
	alice_intercept={"iv": "7e571ec7b33a79a1981c886bdf1a9121", "encrypted_flag": "d3f75638ee1352101e6c709469b458dd778461cbbfc7f6b55674a3cf4ebbef49"}
	# inv_shared = gmpy2.invert(shared_key, p)
	shared_secret = shared_key
	iv = alice_intercept["iv"]
	ciphertext = alice_intercept["encrypted_flag"]

	return decrypt_flag(shared_secret, iv, ciphertext)

def export_grade():
	# Intercepted from Alice: {"supported": ["DH1536", "DH1024", "DH512", "DH256", "DH128", "DH64"]}
	# Send to Bob: {"supported": ["DH64"]}                                                            
	# Intercepted from Bob: {"chosen": "DH64"}
	# Send to Alice: {"chosen": "DH64"}
	# Intercepted from Alice: {"p": "0xde26ab651b92a129", "g": "0x2", "A": "0xcf38b06c090200be"}
	# Intercepted from Bob: {"B": "0x2cbaef9520e4c183"}
	# Intercepted from Alice: {"iv": "8cae6515148c7ef89ca84c74218a59d3", "encrypted_flag": "2eeb3b5e860460b2d0692181f4c1f4ddedd1933b682e9a7e14caeef9bfd66949"}
	alice ={"p": "0xde26ab651b92a129", "g": "0x2", "A": "0xcf38b06c090200be"}
	bob = {"B": "0x2cbaef9520e4c183"}
	message = {"iv": "8cae6515148c7ef89ca84c74218a59d3", "encrypted_flag": "2eeb3b5e860460b2d0692181f4c1f4ddedd1933b682e9a7e14caeef9bfd66949"}
	# brute force attack
	p = int(alice["p"][2:], 16)
	g = int(alice["g"][2:], 16)
	A = int(alice["A"][2:], 16)
	B = int(bob["B"][2:], 16)

	# Not regular log, DISCRETE log (means you include modulo)
	# x = math.log(A, g)
	print(p, A)
	# y = math.log2(B)
	# found on website
	shared_key = pow(B, 6224614707770108603, p)
	return decrypt_flag(shared_key, message["iv"], message["encrypted_flag"])

def static_client():
	alice = {"p": "0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff", "g": "0x02", "A": "0x24ea8a67a2ec98cf410740d72f402aae0200a7a2fbfa38b5c73b2b315f437283893e393863fae7319657ee0410eea528ca72705a774e34dbe95aeeacea9c9a572728c580ab26df22ae0c6f60ad08eda6cb8693236843132dfec11486263e08873feb0af0331f86768deb30f7cb0e2bf5cd84d848694be49c7aa03453fb41142b2d3002634d045b8a60d0338344cb02028a4559efe6fcb9df2bb9af397964d3a673c36f5385b6b179572e533b4634c8d2959affc0b1a58bc583ebd1944e912607"}
	bob = {"B": "0x8d79b69390f639501d81bdce911ec9defb0e93d421c02958c8c8dd4e245e61ae861ef9d32aa85dfec628d4046c403199297d6e17f0c9555137b5e8555eb941e8dcfd2fe5e68eecffeb66c6b0de91eb8cf2fd0c0f3f47e0c89779276fa7138e138793020c6b8f834be20a16237900c108f23f872a5f693ca3f93c3fd5a853dfd69518eb4bab9ac2a004d3a11fb21307149e8f2e1d8e1d7c85d604aa0bee335eade60f191f74ee165cd4baa067b96385aa89cbc7722e7426522381fc94ebfa8ef0"}
	alice_response = {"iv": "c688cab71d424575b7e340d3d314ba42", "encrypted": "195af483bb299c26a8ceee30c5ed9dff835709773e70d7e3f8f03f22e1a0f833"}

	p = int(alice["p"][2:], 16)
	g = 2
	A = int(alice["A"][2:], 16)
	B = int(bob["B"][2:], 16)

	privateKey1 = 6
	# temp = hex(pow(2,6,11))
	temp = hex(pow(g, privateKey1, p))
	send_to_bob = "{\"p\": \"" + "0xb" + "\", \"g\": \"0x2\", \"A\": " + "\"" + str(temp) + "\"}"
	# send_to_bob = "{\"p\": \"" + alice["p"] + "\", \"g\": \"0x2\", \"A\": " + "\"" + str(temp) + "\"}"
	print(send_to_bob)

	print(p-1)
	# note, prime factors of p-1 = 
	# 2
	# 1205156213460516294276038011098783037428475274251229971327058470979054415841306114445046929130670807336613570738952006098251824478525291315971365353402504611531367372670536703348123007294680829887020513584624726600189364717085162921889329599071881596888429934762044470097788673059921772650773521873603874984881875042154463169647779984441228936206496905064565147296499973963182632029642323604865192473605840717232357219244260470063729922144429668263448160459816959

	bob2= {"B": "0x9"}
	bob_response= {"iv": "0817ee5330d4f339e46fe45884aaa9d7", "encrypted": "71f8fb5deaf4abadd7fcd3fdfec3bb6a578e03fc276481d092f8975ca1bc92653c859f65e5844ebd55893a32373a892f97efdaee9c3c4f65e867b0eedae79dcb863f5e4c400e25d66c15e2b4aadfbfb5"}
	# bob_response = {"iv": "f6df5d934bea224b3b7d0439aa672272", "encrypted": "710cf88869f3fcb909d4e65bd0e7467c9983509d71fcd94525b00df0e3356d81025586d39e2730a08e760280dafe058be6f01fd4549bba642ceaf1e53cb1c914fe7e604ce239a73f572b2f27d60c73d8"}
	# alice_public = pow()
	# return decrypt_flag(pow( int(bob2["B"], 16), 6, p), bob_response["iv"], bob_response["encrypted"])
	return decrypt_flag(pow( int(bob2["B"], 16), 6, 11), bob_response["iv"], bob_response["encrypted"])


def main():
	# print("Man in the Middle 1: ", parameter_injection())
	# print("Man in the Middle 2: ", export_grade())
	print("Man in the Middle 3: ", static_client())

if __name__ == '__main__':
	main()