testc = '2d0fb3a56aa66e1e44cffc97f3a2e030feab144124e73c76d5d22f6ce01c46e73a50b0edc1a2bd243f9578b745438b00720870e3118194cbb438149e3cc9c0844d640ecdb1e71754c24bf43bf3fd0f9719f74c7179b6816e687fa576abad1955'
flagc = '2767868b7ebb7f4c42cfffa6ffbfb03bf3b8097936ae3c76ef803d76e11546947157bcea9599f826338807b55655a05666446df20c8e9387b004129e10d18e9f526f71cabcf21b48965ae36fcfee1e820cf1076f65'

def hex(a):
	ret = []
	for i in range(0,len(a), 2):
		ret.append(int(a[i:i+2], 16))
	return ret

def using_flag(xor, flag):
	test = ""
	flag_ord = [ord(i) for i in flag]
	for i in range(len(flag_ord)):
		test += chr(flag_ord[i] ^ xor[i])
	print(test)


def using_test(xor, test):
	flag = ""
	test_ord = [ord(i) for i in test]
	for i in range(len(test_ord)):
		flag += chr(test_ord[i] ^ xor[i])
	print(flag)

testa = hex(testc)
flaga = hex(flagc)

flag = "CHTB{stream_ciphers_with_reused_keystReams_are_vulnerable_to_known_plaintext_attacks"

# print(testa, flaga)
xor = [flaga[i] ^ testa[i] for i in range(len(flaga))]

using_flag(xor, flag)
using_test(xor, "I alone cannot change the world, but i can cast a stone across the water to create ma")

# for i in range(32, 128):
# 	print(chr(i))
# 	using_test(xor, "I alone " + chr(i))





