''' The ciphertext is:
Ne iy nytkwpsznyg nth it mtsztcy vjzprj zfzjy rkhpibj nrkitt ltc tnnygy ysee itd tte cxjltk

Ifrosr tnj noawde uk siyyzre, yse Bnretèwp Cousex mls hjpn xjtnbjytki xatd eisjd

Iz bls lfwskqj azycihzeej yz Brftsk ip Volpnèxj ls oy hay tcimnyarqj dkxnrogpd os 1553 my Mnzvgs Mazytszf Merqlsu ny hox moup Wa inqrg ipl. Ynr. Gotgat Gltzndtg Gplrfdo 

Ltc tnj tmvqpmkseaznzn uk ehox nivmpr g ylbrj ts ltcmki my yqtdosr tnj wocjc hgqq ol fy oxitngwj arusahje fuw ln guaaxjytrd catizm tzxbkw zf vqlckx hizm ceyupcz yz tnj fpvjc hgqqpohzCZK{m311a50_0x_a1rn3x3_h1ah3xf966878l}

Tnj qixxe wkqw-duhfmkseej ipsiwtpznzn uk l puqjarusahjeii htpnjc hubpvkw, hay rldk fcoaso 1467 be Qpot Gltzndtg Fwbkwei.

Zmp Volpnèxj Nivmpr ox ehkwpfuwp surptorps ifwlki ehk Fwbkwei Jndc uw Llhjcto Htpnjc.

It 1508, Ozhgsyey Ycizmpmozd itapnzjo tnj do-ifwlki eahzwa xjntg (f xazwtx uk dhokeej fwpnfmezx) ehgy hoaqo lgypr hj l cxneiifw curaotjyt uk ehk Atgksèce Inahkw.

Merqlsu’x deityd htzkrje avupaxjo it 1555 fd a itytosfaznzn uk ehk ktryy. Ehk qzwkw saraps uk ehk fwpnfmezx lrk szw ymtfzjo rklflgwwy, hze tnj llvmlbkyd ati ehk nydkc wezypry fce sniej gj mkfys uk l mtjxotnn kkd ahxfde, cmtcn hln hj oilkprkse woys eghs cuwceyuznjjyt.
'''

# Breaking the vignere cipher

import binascii
from collections import Counter, defaultdict

# Hamming distance
def ham(a, b):
	count = 0
	for i in range(len(a)):
		try:
			if a[i] != b[i]:
				count += 1
		except:
			break
	return count


# utilize kasiski test / own variation
# This is used to predict the key size used in the vignere cipher, and does so by iterating through some random key size
# Then, in two for loops: for each chunk of letters of this key size in the cipher that was not seen previously,
# iterate through each subsequent chunk of letters of this key size and check the hamming distance
# Return the value with the lowest average hamming distance 
def best_size(text):
	d = Counter() # keep track of the i values
	zero = defaultdict(list) # keep track of repeated words
	visited = Counter() # keep track of all the visited values
	for i in range(2,10):
		count = 0
		dis = 0
		for j in range(0,len(text),i):	
			base_word = text[j:j+i]
			if base_word not in visited:
				for k in range(j+i, len(text), i):
					compare_with = text[k:k+i]
					if (len(base_word) == len(compare_with)):
						dis += ham(base_word , compare_with)
						if (dis == 0): 
							zero[i].append(compare_with)
						# print(base_word, compare_with)
						count += i
						# print(i, dis, count)
				# print(i, count)
				visited[text[j:j+i]] = 1
		# print(dis, count)
		d[ i ] += (dis / count)
		

	print(d)
	print(zero)
	return min(d, key=lambda x: d[x])

# Calculate the letter frequency
def freq_cal(a):
	d = Counter()
	for i in a:
		d[i] += 1
	for i in d.keys():
		d[i] /= len(a)
		d[i] *=100
	return d

# Calculate score of input dictionary called letters by taking absolute value
def score(letters):
	d = {'e': 12.70, 't': 9.06, 'a': 8.17, 'o': 7.51, 'i': 6.97, 'n': 6.75, 's': 6.33, 'h': 6.09, 'r': 5.99, 'd': 4.25, 'l': 4.03, 'c': 2.78, 'u': 2.76, 'm': 2.41, 'w': 2.36, 'f': 2.23, 'g': 2.02, 'y': 1.97, 'p': 1.93, 'b': 1.29, 'v': 0.98, 'k': 0.77, 'j': 0.15, 'x': 0.15, 'q': 0.10, 'z': 0.07}	
	# for i in letters.keys():
	score = 0
	for i in letters.keys():
		try:
			score += abs(letters[i] - d[i])
		except:
			return 1000
	return score

def main():
	with open('file.txt', 'r') as f:
		file = f.read().rstrip().lower()
	
	letters = ''
	alphabet = "abcdefghijklmnopqrstuvwxyz" # note: using this instead of isalpha is better because no special characters are included
	for i in file:
		if i in alphabet:
			letters += i

	# print(letters, len(letters))

	best_val = best_size(letters)
	print(best_val)

	d = defaultdict(list)
	for i in range(len(letters)):
		d[i%best_val].append(letters[i])

	print(d)
	# frequency analysis attack after this point
	# for each potential key value, generate a list of letters from that key via xor operation
	# get the letter frequency and then score it based on expected frequency and take the top values with the high score
	best_vals = {i:1000 for i in d.keys()}
	best_key = Counter()
	print(best_vals)
	for num in d:
		for i in range(97, 124):
			a = []
			# get all the xor values
			for char in d[num]:
				temp = chr((ord(char) - i) % 26 + 97)
				a.append(temp)
			freq = freq_cal(a)
			current_score = score(freq)
			if (current_score < best_vals[num]):
				best_vals[num] = current_score
				best_key[num] = chr(i)

	key = ''
	for i in sorted(best_key):
		print(best_key[i])
		key += best_key[i]

	# Apply the key
	index = 0
	for i in range(len(file)):
		if file[i] in alphabet:
			file = file[:i] + chr((ord(file[i]) - ord(key[index]))% 26 + 97) + file[i+1:]
			index += 1
			index %= best_val
	print(file)



if __name__ == '__main__':
	main()
