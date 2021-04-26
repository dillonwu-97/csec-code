import hashlib

salt = "e361bfc569ba48dc"
i = 0
while 1:
	print(i)
	h = hashlib.md5((salt + str(i)).encode()).hexdigest()
	if h[:2] == '0e' and h[2:].isdigit():
		print("FOUND ", i, h)
		break
	i+=1

