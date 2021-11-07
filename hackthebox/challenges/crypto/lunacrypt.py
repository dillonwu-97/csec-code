import math
from random import randint, seed
from time import time, process_time

strchr = lambda x: chr(x)
strbyt = lambda x, y=0: ord(x[y])
bitlst = lambda x, y: x << y
bitrst = lambda x, y: x >> y
bitext = lambda x, y, z=1: bitrst(x, y) & int(math.pow(2, z) - 1)
bitxor = lambda x, y: x ^ y
bitbor = lambda x, y: x | y
btest  = lambda x, y: (x & y) != 0
mthrnd = lambda x, y: randint(x, y)
mthrsd = lambda x: seed(x)
osltim = lambda: int(time())
oslclk = lambda: process_time()


FL_NEGATE = bitlst(1, 1)
FL_UNUSED3 = bitlst(1, 2)
FL_XORBY6B = bitlst(1, 3)
FL_XORBY3E = bitlst(1, 4)
FL_UNUSED2 = bitlst(1, 5)
FL_SWAPBYTES = bitlst(1, 6)
FL_UNUSED1 = bitlst(1, 7)

currtime = osltim()
while True:
	if osltim() - currtime != 0:
		break

mthrsd(osltim() + oslclk() * 1000)

def ValidateChar(char):
	if type(char) is str and len(char) == 1:
		char = strbyt(char)
	return char

def GenerateFlag():
	finalflag = 0
	if mthrnd(0, 1) == 1:
		finalflag = bitbor(finalflag, FL_SWAPBYTES)
	if mthrnd(0, 1) == 1:
		finalflag = bitbor(finalflag, FL_NEGATE)
	if mthrnd(0, 1) == 1:
		finalflag = bitbor(finalflag, FL_XORBY6B)
	if mthrnd(0, 1) == 1:
		finalflag = bitbor(finalflag, FL_XORBY3E)
	if mthrnd(0, 1) == 1:
		finalflag = bitbor(finalflag, FL_UNUSED3)
	if mthrnd(0, 1) == 1:
		finalflag = bitbor(finalflag, FL_UNUSED2)
	if mthrnd(0, 1) == 1:
		finalflag = bitbor(finalflag, FL_UNUSED1)

	return finalflag

def CheckFlag(f, flag):
	return btest(f, flag)

def ESwapChar(char):
	char = ValidateChar(char)
	THIS_MSB = bitext(char, 4, 4)
	THIS_LSB = bitext(char, 0, 4)

	return strchr(bitbor(bitxor(THIS_MSB, 0x0D), bitxor(bitlst(THIS_LSB, 4), 0xB0)))

def XorBy6B(char):
	char = ValidateChar(char)
	
	return strchr(bitxor(char, 0x6B))

def XorBy3E(char):
	char = ValidateChar(char)
	
	return strchr(bitxor(char, 0x3E))

def NegateChar(char):
	char = ValidateChar(char)
	
	return strchr(255 - char)

def reverse():
	a = {}
	b = {}
	c = {}
	d = {}
	for j in range(0,255):
		# print(j)
		i = chr(j)
		temp = ord(ESwapChar(i))
		# print("temmp is ", temp)
		a[ temp ] = j

		temp = ord(XorBy6B(i))

		b[ temp ] = j

		temp = ord(XorBy3E(i))
		c[ temp ] = j

		temp = ord(NegateChar(i))
		d[ temp ] = j
	return a, b, c, d




FLAGS = []
CHARS = []

def AppendFlag(flag):
	FLAGS.append(strchr(bitxor(flag, 0x4A)))

def EncryptCharacter(char):

	char = ValidateChar(char)
	flag = GenerateFlag()
	print(char, flag, 'THE CHANGE IS ')
	if CheckFlag(flag, FL_SWAPBYTES):
		print('one')
		char = ESwapChar(char)
	if CheckFlag(flag, FL_NEGATE):
		print('two')
		char = NegateChar(char)
	if CheckFlag(flag, FL_XORBY6B):
		print('three')
		char = XorBy6B(char)
	if CheckFlag(flag, FL_XORBY3E):
		print('four')
		char = XorBy3E(char)
	print(ord(char), flag)

	return char, flag

def _Encrypt(string):

	for i in range(0, len(string)):
		char, flag = EncryptCharacter(strbyt(string, i)) # encrypt with order of ith character

		if type(char) is int:
			char = strchr(char)

		CHARS.append(char)
		AppendFlag(flag)
	print(CHARS)

def Encrypt(string):
	_Encrypt(string)

	output = [f"{str(ord(v))} {str(ord(FLAGS[i]))}" for i, v in enumerate(CHARS)]
	print(output)
	print(" ".join(output))
	# file = open("output.txt", "w")
	# file.write(' '.join(output))
	# file.close()
	return output

# Need to split this into two different ones
print(ord("h"), ord("i"))
output = Encrypt("him")
a,b,c,d = reverse()
print("-----OUTPUT-----")
print(output)
chars_array = [ int(i.split(' ')[0]) for i in output]
flags_array = [ int(i.split(' ')[1]) ^ 0x4A for i in output]
ret = []

ciphertext = f = open('output.txt').read().split(' ')
chars_array = [ int( ciphertext[i]) for i in range (0,len(ciphertext), 2)]
flags_array = [ int( ciphertext[i])^ 0x4A  for i in range (1,len(ciphertext), 2)]

print(chars_array)
print(flags_array)
# print(a, b, c, d)
for i in range(len(flags_array)):
	flag = flags_array[i]
	char = chars_array[i]
	if CheckFlag(flag, FL_XORBY3E):
		char = c[ char]
	if CheckFlag(flag, FL_XORBY6B):
		char = b[ char]
	if CheckFlag(flag, FL_NEGATE):
		char = d[ char]
	if CheckFlag(flag, FL_SWAPBYTES):
		char = a[ char]
	
	
	
	
	print(char)
	ret.append(char)
print(ret)
print (''.join([chr(i) for i in ret]))
# print(a)


