import random 
lr = '\x64'
chains = [0x74, 0x68, 0x69, 0x73, 0x20, 0x69, 0x73, 0x20, 0x61, 0x20, 0x74, 0x72, 0x6f, 0x6c, 0x6c]
db = '\x6e'
ef = '\x63'
chars = []
keys = [0x70, 0x61, 0x73, 0x73, 0x77, 0x6f, 0x72, 0x64, 0x21, 0x21]
nn = '\x61'
lock_pick = random.randint(0, 0x3e8)
lock = lock_pick * 2
password = [0x69, 0x74, 0x73, 0x20, 0x6e, 0x6f, 0x74, 0x20, 0x74, 0x68, 0x61, 0x74, 0x20, 0x65, 0x61, 0x73, 0x79]
lock = lock + 10
ty = '\x61'
lock = lock / 2
auth = [0x6b, 0x65, 0x65, 0x70, 0x20, 0x74, 0x72, 0x79, 0x69, 0x6e, 0x67]
lock = lock - lock_pick
gh = '\x6e'

for key in keys:
	keys_encrypt = int(lock) ^ key
	# keys_encrypt = key
	chars.append(keys_encrypt)
# for chain in chains:
# 	# chains_encrypt = chain + 0xA
# 	chains_encrypt = chain
# 	chars.append(chains_encrypt)
aa = '\x61'
rr = '\x6f'
slither = aa + db + nn + ef + rr + gh + lr + ty

print('solving...')
a = [chars, chains, keys, password, auth]
for i in a:
	out = []
	for h in i:
		out.append(chr(int(h)))
	print("".join(out))
print("slither is ", slither)
print("lockpick is ", lock_pick, " and lock is ", lock)

print('lock picking password')
plock = []
for i in password:
	plock.append(chr(int(lock) ^ i))
print(plock)

print('lock picking auth')
pauth = []
for i in auth:
	pauth.append(chr(int(lock) ^ i))
print(pauth)