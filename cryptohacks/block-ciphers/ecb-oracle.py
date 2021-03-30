from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from pwn import *
import json
import requests
import binascii


def encrypt(plaintext):
    plaintext = bytes.fromhex(plaintext)

    padded = pad(plaintext + FLAG.encode(), 16)
    cipher = AES.new(KEY, AES.MODE_ECB)
    try:
        encrypted = cipher.encrypt(padded)
    except ValueError as e:
        return {"error": str(e)}

    return {"ciphertext": encrypted.hex()}

url = 'http://aes.cryptohack.org/ecb_oracle/encrypt/'

def find_size():
	default = 64
	for i in range(1,16):
		payload = (b'B' * i).hex()
		r = requests.get(url + payload)
		j = json.loads(r.text)
		# print(j)
		if len(j['ciphertext']) != default:
			return i - 1


def main():
	# max_size = find_size()
	# print("flag size is ", 64 - max_size) # 58 bytes
	flag = 'crypto{p3n6u1n' # solution


	# payload and current variables are used to generate each subsequent value used for comparisons
	compare_val = 'A' # size = 8 bytes since we know the start of the flag will be "crypto{"
	size = 15
	multiplier = 1
	r = requests.get(url + compare_val.encode().hex()) # Note: cannot use empty string as input
	j = json.loads(r.text)
	current = j['ciphertext'][:32] # this contains the value we are trying to find
	
	# payload is used for testing purposes
	payload =  'Acrypto{p3n6u1n' # length is 16
	for i in range(58):
		for c in range(32, 128):
			print(chr(c))
			# the temp variable is the current payload + variable
			temp = (payload + chr(c)).encode().hex() # this contains what we are trying to find
			r = requests.get(url + temp)
			j = json.loads(r.text)
			# print("payload ciphertext: " , j['ciphertext'][ (multiplier-1) * 32 :multiplier * 32])
			# print(current, j['ciphertext'][ (multiplier-1) * 32 :multiplier * 32])
			if j['ciphertext'][ (multiplier-1) * 32 :multiplier * 32] == current:
				print("FOUND", c)
				letter = chr(c)
				flag += letter
				payload = payload[1:] + chr(c)
				print("payload is ", payload)

				compare_val = compare_val[1:]
				if len(compare_val) == 0:
					print("inside compare")
					compare_val = 'A' * 16 # 16 'A'
					multiplier += 1
					payload = 'A' * 16 + flag # 16 'A' + 15 characters of discovered flag
				print("compare_val is ", compare_val)
				r = requests.get(url + compare_val.encode().hex())
				j = json.loads(r.text)
				current = j['ciphertext'][ (multiplier-1) * 32 : multiplier * 32]
				# print("basis: ", j['ciphertext'][ (multiplier-1) * 32 : multiplier * 32])

				# move onto the next chunk
				print("flag is ", flag)
				break



if __name__ == '__main__':
	main()

