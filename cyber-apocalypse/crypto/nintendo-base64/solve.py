import base64
with open('output.txt', 'r') as f:
	file = f.read().replace(" ","")


for i in range(10):
	try:
		file = base64.b64decode(file)
		print(file)
	except:
		break
# CHTB{3nc0d1ng_n0t_3qu4l_t0_3ncrypt10n}