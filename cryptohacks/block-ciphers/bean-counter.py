import requests
import json
import binascii

def xor_hex(a, b):
	temp = int(a, 16) ^ int(b, 16)
	return hex(temp)[2:].zfill(2)

def main():
	url = 'http://aes.cryptohack.org/bean_counter/encrypt/'
	r = requests.get(url)
	j = json.loads(r.text)
	encrypted = j['encrypted']

	# enc_pic = bytes.fromhex(encrypted)
	enc_pic = binascii.unhexlify(encrypted)

	header = '89504e470d0a1a0a0000000d49484452'
	# 49454e44ae426082
	# footer = '426082'

	# we have the first 11 bytes of the key
	print(len(encrypted), len(encrypted)% 32)

	key_1 = encrypted[:32]
	# key_2 = encrypted[-6:]
	# print(key_2)
	key = ''
	for i in range(0,len(key_1), 2):
		temp = xor_hex(key_1[i:i+2], header[i:i+2])
		key += temp

	# for i in range(0, len(key_2), 2):
	# 	temp = xor_hex(key_2[i:i+2], footer[i:i+2])
	# 	key += temp

	print(key)

	decrypted = ''
	track = 0
	for i in range(0,len(encrypted),2):
		temp = xor_hex(encrypted[i:i+2], key[track:track+2])
		track += 2
		if (track >= len(key)): track = 0
		decrypted += temp

	d = bytes.fromhex(decrypted)

	with open('bc.png', 'wb') as f:
		f.write(d)




if __name__ == '__main__':
	main()


# from Crypto.Cipher import AES


# KEY = ?


# class StepUpCounter(object):
#     def __init__(self, value=os.urandom(16), step_up=False):
#         self.value = value.hex()
#         self.step = 1
#         self.stup = step_up

#     def increment(self):
#         if self.stup:
#             self.newIV = hex(int(self.value, 16) + self.step)
#         else:
#             self.newIV = hex(int(self.value, 16) - self.stup)
#         self.value = self.newIV[2:len(self.newIV)]
#         return bytes.fromhex(self.value.zfill(32))

#     def __repr__(self):
#         self.increment()
#         return self.value



# @chal.route('/bean_counter/encrypt/')
# def encrypt():
#     cipher = AES.new(KEY, AES.MODE_ECB)
#     ctr = StepUpCounter()

#     out = []
#     with open("challenge_files/bean_flag.png", 'rb') as f:
#         block = f.read(16)
#         while block:
#             keystream = cipher.encrypt(ctr.increment())
#             xored = [a^b for a, b in zip(block, keystream)]
#             out.append(bytes(xored).hex())
#             block = f.read(16)

#     return {"encrypted": ''.join(out)}
