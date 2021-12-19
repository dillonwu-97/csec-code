'''
Write a function that takes two equal-length buffers and produces their XOR combination.

If your function works properly, then when you feed it the string:

1c0111001f010100061a024b53535009181c
... after hex decoding, and when XOR'd against:

686974207468652062756c6c277320657965
... should produce:

746865206b696420646f6e277420706c6179
'''

import sys

s1 = sys.argv[1]
s2 = sys.argv[2]
s3 = ""

for i in range(len(s1)):
	s3 +=hex(int(s1[i],16) ^ int(s2[i],16))[2:]


print(s3)
