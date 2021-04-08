from collections import Counter

def main():
	alph = 'abcdefghijklmnopqrstuvwxyz'
	f = open('cm02.txt').read()
	d = Counter(f)
	count = 0
	replace_with = {}
	for i in d:
		if len(i.encode().hex()) > 5:
			replace_with [i] =  alph[count]
			count += 1
	
	for i in range(len(f)):
		# print(i)
		if len(f[i].encode().hex()) > 5:
			f = f[:i] + replace_with[f[i]] + f[i+1:]
	print(f)

	# put output into substitution cipher cracker
	# flag: frequently_substitute_frowny_face_for_smiley_face


if __name__ == '__main__':
	main()