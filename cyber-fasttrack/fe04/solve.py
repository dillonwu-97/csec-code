f = open('50k-users.txt')
# The username you are looking for has x as the 3rd character, followed immediately by a number from 2 to 6, it has a Z character in it and the last character is S.
for i in f:
	i = i.strip()
	if i[2] == 'x' and 'Z' in i and i[-1] == 'S':
		try:
			if int(i[3]) in range(2,7):
				print(i)
		except:
			continue
