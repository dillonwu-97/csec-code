'''
Solution:
Decrypted value is: Cooking MC's like a pound of bacon

Problem:
The hex encoded string:

1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736
... has been XOR'd against a single character. Find the key, decrypt the message.
'''

import os
import binascii


e = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'

def score(s):
	v = ['a','e','i','o','u']
	count = 0
	for i in s:
		if i in v:
			count += 1
	return count

combinations = []
# byte_list = []
for key in range(0,128):
	current = str(hex(key)[2:]) * len(e)
	xor = ""
	# b = b''
	for i in range(len(e)):
		xor_val = int(current[i], 16) ^ int(e[i], 16)
		# b += bytes([xor_val])
		xor += hex( xor_val )[2:]
		# xor += hex( int(current[i], 16) ^ int(e[i], 16) )
	combinations.append(xor)
	# byte_list.append(b)

ret_list = []
for i in range(len(combinations)):
	ret_list.append(binascii.unhexlify(combinations[i]))
	# try:
	# 	out = bytearray.fromhex(combinations[i]).decode('utf-8')
	# except:
	# 	continue
	# ret_list.append(out)

score_list = []
for i in ret_list:
	score_list.append(score(str(i)))

z = zip(ret_list, score_list)
z= sorted(z, key = lambda a: -1 * a[1])
print(list(z)[:5])