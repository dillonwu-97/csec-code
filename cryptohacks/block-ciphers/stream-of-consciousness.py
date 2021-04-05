import requests
import json

# a, b = ciphertext
# c, d = plaintext
def guess_and_check(a, b, c, d):
	plain = []
	for i in range(0, min(len(a), len(b)), 2):
		temp = int(a[i:i+2], 16) ^ int(b[i:i+2], 16)
		plain.append(temp)
	plainhex = ''.join([hex(i)[2:].zfill(2) for i in plain])
	alph = ' abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

	# start point is after the end of known characters
	ret = ""
	for i in range(len(c)):
		temp = ord(c[i]) ^ ord(d[i])
		# temp = chr(temp)
		ret += hex(temp)[2:].zfill(2)

	print(ret)
	print(plainhex)





def main():
	STEP_1 = True
	STEP_2 = False # <-- step 2 turns out to be useless and it's faster to just examine the plaintext instead

	url = 'http://aes.cryptohack.org/stream_consciousness/encrypt/'
	r = requests.get(url)
	j = json.loads(r.text)

	random_start = j["ciphertext"]

	### Notes / thoughts:
	# different ciphertext for same plaintext? so maybe the counter is not the same?
	# ea7a75f652e77035e1c074fcc0930a51bfccffd21fc327957361598523c4451e53ff379128f0ff82d17c7ebee54f08f718bbe361611e7b49408da9f9fea73c9df08006010624b4c554c8434dc9841e64581403e3ab375e94de6b084f7e
	# c5677ae30aa87b2cbddb20a9ded9011cb4d6a9de0a9417ca614a1fda7a9f5e43
	guess = "crypto{"
	guess = "I shall "
	guess = "Our? Why "
	guess = "Why do the "
	guess = "And I shall "
	guess = "I shall lose "
	guess = "These horses, "
	guess = "Perhaps he has "
	guess = "But I will show "
	guess = "And I shall ignore "
	guess = "Would I have believe"
	guess = "I'm unhappy, I deserve"
	guess = "I shall lose everything "
	guess = "Love, probably? They don't "
	guess = "I shall lose everything and "
	guess = "How proud and happy he'll be "
	guess = "Perhaps he has missed the train "
	guess = "I shall lose everything and not "
	guess = "As if I had any wish to be in the "

	# crypto{k3y57r34m_r3u53_15_f474l}

	if STEP_1:
		while (1):
			r = requests.get(url)
			j = json.loads(r.text)
			current = j["ciphertext"]
			plaintext_xored = []
			for i in range(0, min(len(random_start), len(current)), 2):
				temp = int(random_start[i: i+2], 16) ^ int(current[i: i+2], 16) # plaintext xored
				plaintext_xored.append(temp)

			res = ''
			for i in range(min(len(guess), len(plaintext_xored))):
				temp = chr(ord(guess[i]) ^ plaintext_xored[i]) # some int value
				res += temp

			print(res)

			# Used below to find the ciphertexts associated with a given plaintext
			if ("crypto" in res):
				print("Found ", res)
				break

	if STEP_2:
		a = "ea7a75f652e77035e1c074fcc0930a51bfccffd21fc327957361598523c4451e53ff379128f0ff82d17c7ebee54f08f718bbe361611e7b49408da9f9fea73c9df08006010624b4c554c8434dc9841e64581403e3ab375e94de6b084f7e"
		b = "e26766e00dea6d26e5cb7bf98c8b5b15cbe9f3c753ce269e266c"
		c = "I shall"
		d = "These h"
		guess_and_check(a,b,c,d)



if __name__ == '__main__':
	main()


{"ciphertext":"ef3570fb1fab6c67e2cd66fb8c8f431499ddeec356c92fdb357b1dce23c4461e5cf5349124ebf7c3c1643dbcbf"}
{"ciphertext":"ef3570fb1fab6c6baeeb32f2c0ca591e98c1bace49c23a82207d10802a8b5b581bf8259128edff90cd222af7f2000ce114f9ea6d7d10"}



{"ciphertext":"f27d66e01be76828fcd170ed80ca411982d7bac85ed53a9235721cce608b5a514cb0099120edfb97cb607ebae81c04e852bbe260364a7b555ec4a6f1eda13c92f0cb08020624b4c50dae474d8790172819120eb0f37f558dce39240123eb961300648dcd398e8f570142559d583ba477fe5adbbfe0b3c6"}