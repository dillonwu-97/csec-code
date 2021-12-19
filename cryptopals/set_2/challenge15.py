'''
PKCS#7 padding validation
Write a function that takes a plaintext, determines if it has valid PKCS#7 padding, and strips the padding off.

The string:

"ICE ICE BABY\x04\x04\x04\x04"
... has valid padding, and produces the result "ICE ICE BABY".

The string:

"ICE ICE BABY\x05\x05\x05\x05"
... does not have valid padding, nor does:

"ICE ICE BABY\x01\x02\x03\x04"
If you are writing in a language with exceptions, like Python or Ruby, make your function throw an exception on bad padding.

Crypto nerds know where we're going with this. Bear with us.
'''


# check if the string has valid padding by taking last character, finding order and going backwards
# issues to consider: if nonpadded string %16 = 0, then there should be 16 characters of \x10 padding
# if the padding ends in \x01 and the string is "ICE ICE BABY\x04\x03\x02\x01", the code will assume
# that \x04\x03\x02 is part of the intended string
# it also assumes that "ICE ICE BABY\x03\x03\x03\x03" is a valid string and that the first \x03 character
# is part of the intended string value
def is_valid(s):
	last_char = s[-1]
	padding_val = ord(s[-1])
	for i in range(padding_val):
		if s[-1 - i] != last_char:
			return False
			# raise ValueError("padding incorrect")
	return True

def strip_padding(s):
	padding_val = ord(s[-1])
	return s[:-padding_val]

def main():
	test_strings = ["ICE ICE BABY\x04\x04\x04\x04", "ICE ICE BABY\x05\x05\x05\x05", "ICE ICE BABY\x01\x02\x03\x04"]
	for i in test_strings:
		if is_valid(i):
			print(i, is_valid(i), strip_padding(i))
		else:
			print(i, is_valid(i))

if __name__ == '__main__':
	main()