# useful 
# https://blog.stayontarget.org/2019/03/decoding-mixed-case-usb-keystrokes-from.html
# https://abawazeeer.medium.com/kaizen-ctf-2018-reverse-engineer-usb-keystrok-from-pcap-file-2412351679f4

f = open('leftovers.txt', 'r')
newmap = {
	2: "PostFail",
	4: "a",
	5: "b",
	6: "c",
	7: "d",
	8: "e",
	9: "f",
	10: "g",
	11: "h",
	12: "i",
	13: "j",
	14: "k",
	15: "l",
	16: "m",
	17: "n",
	18: "o",
	19: "p",
	20: "q",
	21: "r",
	22: "s",
	23: "t",
	24: "u",
	25: "v",
	26: "w",
	27: "x",
	28: "y",
	29: "z",
	30: "1",
	31: "2",
	32: "3",
	33: "4",
	34: "5",
	35: "6",
	36: "7",
	37: "8",
	38: "9",
	39: "0",
	40: "Enter",
	41: "esc",
	42: "del",
	43: "tab",
	44: "space",
	45: "-",
	47: "{",
	48: "}",
	49: "\\",         
	50: " ",         
	51: ";",         
	52: "'",
	53: "`",
	54: ",",
	55:".",
	56: "/",
	57: "CapsLock",
	79: "RightArrow",
	80: "LetfArro"
}
a = []
case = []
for i in f:
	try:
		letter = i.strip('\r\n')
		# print(letter)
		if letter[1:3] == '02':
			case.append('x')

		elif letter[1:3] == '00':
			print(letter)
			case.append('y')

		a.append(int(letter[5:7],16))
	except:
		continue
ret = ''
for index, i in enumerate(a):
	if i in newmap and len(newmap[i]) == 1:
		if case[index] == 'x':
			print('x', newmap[i])
			if newmap[i] == '-': ret += '_'
			else: ret += newmap[i].upper()
		else:
			print(newmap[i])
			ret+= newmap[i]
	elif i in newmap and newmap[i] == "space":
		ret += ' '
	elif i == 42:
		print( 'DELETE')
		ret = ret[:-1]
	elif i == 57:
		print('CAPSLOCK')
	elif i not in newmap and i != 0:
		print(i)
		continue
print(ret)
# CHTB{a_plac3_fAr_fAr_away_fr0m_earth}


