import binascii
import string
from collections import Counter
import math

def decrypt_xor(s):
	ret_list = []
	ascii_val = []
	# 33-126 is ascii range i think
	for key in range(33,126): # ascii range
		xor = ""
		# print(key, len(s))
		for i in range(0,len(s),2):
			# xor_val = int(str(key), 16) ^ int(s[i:i+2], 16)
			# the code above does not do what u expect; it takes in the number in hex and converts it to decimal
			# for example, if key = 20, output = 33 because 20 is thought to be in base 16
			# int(s[i:i+2], 16) converts a base 16 hex to a decimal
			xor_val = key ^ int(s[i:i+2], 16)
			# if key == 21:
			# 	print(int(str(key), 16), xor_val, hex( xor_val )[2:].zfill(2))
			# print(hex(xor_val))
			xor += hex( xor_val )[2:].zfill(2)
		# print(xor)
		try:
			ret_list.append(binascii.unhexlify(xor))
			ascii_val.append(chr(key))
		except:
			continue
	return ret_list, ascii_val

def word_score(s):
	freq = {'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75, 'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25, 'L': 4.03, 'C': 2.78, 'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23, 'G': 2.02, 'Y': 1.97, 'P': 1.93, 'B': 1.29, 'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15, 'Q': 0.10, 'Z': 0.07}
	d = Counter()
	for i in range(len(s)):
		d[s[i]] += 1
	total = sum(d.values())
	distance = 0
	spec_count = 0
	space_count = 0
	for k in d:
		d[k] = d[k]/ total * 100
		if k == ' ':
			space_count += 1
			continue
		if k.upper() in freq:
			distance += abs(freq[k.upper()] - d[k])
		else:
			spec_count+=1
			distance += d[k]**2
	if spec_count > len(s) - spec_count or space_count == 0:
		distance = 1000
	return distance


def vowel_count(s):
	v = ['a','e','i','o','u']
	count = 0
	for i in s:
		if i in v:
			count += 1
		# elif not i.isalnum():
		# 	return 0
	return count

def isEnglish(s):
	s = s.strip().replace(' ','')
	return s.translate(str.maketrans('', '', string.punctuation)).isalnum()

def solve(input):		
	ret_list, ascii_val = decrypt_xor(input)
	str_scores = []
	for s in ret_list:
		s = str(s)

		# if isEnglish(s):
		if '\\x' in s:
			str_scores.append(1000)
		else:
			str_scores.append(word_score(s))
		# else:
		# 	str_scores.append(1000)

	# print(max(str_scores))
	z = zip(ret_list, str_scores, ascii_val)
	z = sorted(z, key = lambda x: x[1])
	zlist = list(z)
	return zlist[:16]
		
