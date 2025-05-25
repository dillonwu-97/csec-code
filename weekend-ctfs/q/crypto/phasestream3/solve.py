def hex(a):
	ret = []
	for i in range(0,len(a), 2):
		ret.append(int(a[i:i+2], 16))
	return ret

f = open('output.txt', 'r').read().split('\n')

test = f[0]
flag = f[1]

test = hex(test)
flag = hex(flag)

plain1 = "No right of private conversation was enumerated in the Constitution. I don't suppose it occurred to anyone at the time that it could be prevented."
plain1 = [ord(plain1[i]) for i in range(len(flag))]

print(test, flag)
plain2 = ''
for i in range(len(flag)):
	plain_xored =  flag[i] ^ test[i]
	plain2 += chr(plain_xored ^ plain1[i])

print(plain2)

# CHTB{r3u53d_k3Y_4TT4cK}