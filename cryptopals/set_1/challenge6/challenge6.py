'''
Solution:
Terminator X: Bring the noise

Task:
It's (file.txt) been base64'd after being encrypted with repeating-key XOR.

Decrypt it.

Here's how:

Let KEYSIZE be the guessed length of the key; try values from 2 to (say) 40.
Write a function to compute the edit distance/Hamming distance between two strings. The Hamming distance is just the number of differing bits. The distance between:
this is a test
and
wokka wokka!!!
is 37. Make sure your code agrees before you proceed.
For each KEYSIZE, take the first KEYSIZE worth of bytes, and the second KEYSIZE worth of bytes, and find the edit distance between them. Normalize this result by dividing by KEYSIZE.
The KEYSIZE with the smallest normalized edit distance is probably the key. You could proceed perhaps with the smallest 2-3 KEYSIZE values. Or take 4 KEYSIZE blocks instead of 2 and average the distances.
Now that you probably know the KEYSIZE: break the ciphertext into blocks of KEYSIZE length.
Now transpose the blocks: make a block that is the first byte of every block, and a block that is the second byte of every block, and so on.
Solve each block as if it was single-character XOR. You already have code to do this.
For each block, the single-byte XOR key that produces the best looking histogram is the repeating-key XOR key byte for that block. Put them together and you have the key.
'''
import binascii
# useful link explaining imports: https://stackoverflow.com/questions/14132789/relative-imports-for-the-billionth-time
# from set1_lib.lib import *
import sys
sys.path.append('..')
from set1_lib import lib
import base64
from collections import defaultdict


def tobin(s):
	# big / little endian
	# return bin(int.from_bytes(s.encode(), 'big'))[2:] # this works for strings but what if input is hex?

	# 
	bin_string = ""
	for i in range(0,len(s),2):
		temp = bin(int(s[i:i+2], 16))[2:].zfill(8)
		bin_string+=temp
		# print(temp, s[i:i+2])
	return bin_string


# assume s1 and s2 are of equal length
def hammingDistance(s1, s2):
	s1 = tobin(s1)
	s2 = tobin(s2)
	# if len(s1) > len(s2):
	# 	s2 = s2.zfill(len(s1))
	# elif len(s2) > len(s1):
	# 	s1 = s1.zfill(len(s2))
	# if(len(s1) != len(s2)):
	# 	print('ALERT')
	# 	print(s1, s2)
	count = 0
	# print(len(s1), len(s2))
	for i in range(len(s1)):
		if s1[i] != s2[i]:
			count +=1
	return count

# good explanation as to why this step works:
# https://crypto.stackexchange.com/questions/8115/repeating-key-xor-and-hamming-distance
# Observation: when doing findBestKey, doing adjacent xor operations between chunks of the hexdump
# reveals parity behavior, i.e. hammingDistance(s[j:j+i], s[j+2*i:j+(3*i)]) results in a minimization 
# for key values that are odd parity, where as hammingDistance(s[j:j+i], s[j+i:j+(2*i)]) results in
# a preference for key values that are even parity
# The key value answer is 29 (which is what we get as the top score for the odd parity option), 
# but it is not what we get as the top score for the even parity option.
def findBestKey(s, keysizes):
	keyNumbers = []
	distanceValues = []
	for i in keysizes:
		# get the average key diff
		# print(i)
		current = 0
		count = 0
		for j in range(0,len(s), 2*i):
			# print(s[j:j+i], s[j+i:j+2*i])
			# if len(s[j:j+i]) == len(s[j+i:j+2*i]):
			try:
				temp = hammingDistance(s[j:j+i], s[j+2*i:j+(3*i)])
				current += temp
				count += 1
			except:
				continue
		current /= count # take the average
		current /= i
		keyNumbers.append(i)
		# distanceValues.append(current)
		distanceValues.append(current)
	return keyNumbers, distanceValues

def main():
	keysizes = [i for i in range(2, 41)]
	filetxt = ''
	
	#################### Test Case ########################
	# print("Hamming distance test 1: ", hammingDistance('this is a test', 'wokka wokka!!!'))
	# return
	# print("Hamming distance test 2: ", hammingDistance('this is a test', 'wokka wokka!!!') / len(tobin('this is a test')))
	# 74 68 69 73 20 69 73 20 61 20 74 65 73 74
	# 77 6f 6b 6b 61 20 77 6f 6b 6b 61 21 21 21
	# print(hammingDistance('7468697320697320612074657374', '776f6b6b6120776f6b6b61212121'))
	#######################################################
	
	# iterate through keysizes to find the 3 with the smallest hamming distance
	with open('file.txt', 'r') as f:
		for i in f:
			filetxt += i.strip('\n').strip('\r')
	
	#################### Test Case ########################
	# b64txt = base64.b64decode(filetxt).hex()
	#######################################################
	filetxt = base64.b64decode(filetxt).hex()

	keyNumbers, distanceValues = findBestKey(filetxt, keysizes)
	z = zip(distanceValues, keyNumbers)
	z = sorted(z)
	print(len(filetxt))
# 	# show the keys with the lowest hamming distance values
	# print(list(z))
	# print(list(z)[:5])
	keyGuesses = []
	for i in list(z[:3]):
		keyGuesses.append(i[1])

	print(keyGuesses)
	keyGuess = keyGuesses[0]
	toTranspose = defaultdict(list)
	for i in range(0,len(filetxt),2*keyGuess):
		for j in range(0, 2*keyGuess, 2):
			# try:
			toTranspose[j//2].append(filetxt[i+j:i+j+2])
			# except:
			# 	break

	for key in toTranspose:
		toTranspose[key] = ''.join(toTranspose[key])
		print(key, len(toTranspose[key]))
	# print(toTranspose)
	solution = []
	for key in toTranspose:
		ret = lib.solve(toTranspose[key])
		print(key, ret[0])
		solution.append(ret[0][0])
	# print(solution)

	statement = []
	for i in range(len(solution[0])):
		for j in range(len(solution)):
			# print(i, j)
			# if i == 99:
			# 	break
			# print(type(solution[j][i]), solution[j][i])
			try:
				statement.append(chr(solution[j][i]))
			except:
				break
	print("".join(statement))





if __name__ == '__main__':
	main()