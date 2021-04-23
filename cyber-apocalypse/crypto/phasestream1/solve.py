a = '2e313f2702184c5a0b1e321205550e03261b094d5c171f56011904'
a = [int(a [i:i+2], 16 ) for i in range(0, len(a), 2)]
print(a)
start = 'CHTB{'
key = []
ret = ''
count = 0
for i in range(len(start)):
	key.append ( ord(start[i]) ^ a[i] )

for i in range(len(a)):
	ret += chr( a[i] ^ key[count] )
	count += 1
	count %= 5

print(ret)

#CHTB{u51ng_kn0wn_pl41nt3xt}
