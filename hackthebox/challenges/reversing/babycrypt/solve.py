start = '3f6435'
s = bytes.fromhex(start).decode()
print(s)

k = 'HTB'
n = ''


for i in range(len(s)):
	n += chr( ord(s[i]) ^ ord(k[i]) )
print(n)

# HTB{x0r_1s_us3d_by_h4x0r!}
