def xor(a, b):
	for i in range(len(a)):
		a[i] = a[i] ^ b
	return a
	

def hex(s):
	ret = []
	for i in range(0, len(s), 2):
		ret.append( int(s[i: i+2], 16) )
	return ret

flag = 0
f = open('output.txt', 'r').read().split('\n')

for i in f:
	print(i)
	for char in range(256):
		temp = xor ( hex( i ), char)
		temp = "".join([chr(i) for i in temp])
		if ("CHTB{" in temp):
			print("FOUND: ", temp)
			flag = 1
			break
	if flag == 1:
		break

# flag CHTB{n33dl3_1n_4_h4yst4ck}
# for i in range(256):
# 	temp = xor(hex())
		
