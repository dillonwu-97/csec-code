'''

Task:
Here is the opening stanza of an important work of the English language:

Burning 'em, if you ain't quick and nimble
I go crazy when I hear a cymbal
Encrypt it, under the key "ICE", using repeating-key XOR.

In repeating-key XOR, you'll sequentially apply each byte of the key; the first byte of plaintext will be XOR'd against I, the next C, the next E, then I again for the 4th byte, and so on.

It should come out to:

0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272
a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f

'''
from set1_lib import lib

def xor(s, key):
	ret = ''
	key *= len(s) // len(key) + len(key)
	# print(key)
	for i in range(len(s)):
		temp = hex(ord(s[i]) ^ ord(key[i]))[2:].zfill(2)
		# print(ord(s[i]), s[i], ord(key[i]), key[i], temp)
		ret += temp
		# print(temp, ord(s[i]), ord(key[i]))
	return ret

def main():
	plaintext = 'Burning \'em, if you ain\'t quick and nimble\nI go crazy when I hear a cymbal'
	ret = xor (plaintext, 'ICE')
	print(ret)
	ans = '0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f'
	for i in range(len(ret)):
		if ans[i] != ret[i]:
			print(i, ans[i], ret[i])
	# print(lib.vowel_count(ans))

if __name__ == '__main__':
	main()