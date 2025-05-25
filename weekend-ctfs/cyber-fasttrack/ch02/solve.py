a = '2e310d15730618003c27392502592f1b016e1b1c364505191302'
b = '27271e1d6f3935381618340a740404152d0063160106490a0a050d013d2'
c = '313c0d45350d0c026f3d236b361120191e373c1c3a080e0c2b04'
d = '1b060c2749020b354105271616532f27772f1c204811111745320b10021717'

# crib = 'the flag is Sh'
crib = 'keep guessing for the fla'
crib = [ord(i) for i in crib]

# guess this first because it is same length
def convert(a):
	return [int(a[i:i+2], 16) for i in range(0,len(a),2)]

a = convert(a)
c = convert(c)

xor = [a[i] ^ c[i] for i in range(len(a))]
print(xor)
temp = "".join(hex(i)[2:].zfill(2) for i in xor)
print(temp)

for i in range(0,len(xor)-len(crib)):
	s = ""
	for j in range(len(crib)):
		# print(j, i+j)
		s += chr(crib[j] ^ xor[i+j])
	print(s)

# the flag is ShimmyShimmyYa
