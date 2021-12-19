'''
Solution: (b'Now that the party is jumping\n', 7)


One of the 60-character strings in this file has been encrypted by single-character XOR.

Find it.
'''

import binascii
import string

def decrypt_xor(s):
	ret_list = []
	for key in range(128):
		current = str(hex(key)[2:]) * len(s)
		xor = ""
		for i in range(len(s)):
			xor_val = int(current[i], 16) ^ int(s[i], 16)
			xor += hex( xor_val )[2:]
	
		ret_list.append(binascii.unhexlify(xor))
	return ret_list

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

def main():
	strings = []
	with open('file.txt', 'r') as f:
		for i in f:
			current = i.strip('\r').strip('\n')
			strings += decrypt_xor(current)
			
	str_scores = []
	for i in strings:
		s = str(i)
		if isEnglish(s):
			if '\\x' in s:
				str_scores.append(0)
			else:
				str_scores.append(vowel_count(s))
		else:
			str_scores.append(0)

	# print(max(str_scores))
	z = zip(strings, str_scores)
	z = sorted(z, key = lambda x: -1 * x[1])
	zlist = list(z)
	for i in range(100):
		print(zlist[i])



if __name__ == '__main__':
	main()

