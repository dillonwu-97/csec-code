import sys
import argparse

OPERATIONS = {
	'🍡': "add",
	'🤡': "clone",
	'📐': "divide",
	'😲': "if_zero",
	'😄': "if_not_zero",
	'🏀': "jump_to",
	'🚛': "load",
	'📬': "modulo",
	'⭐': "multiply",
	'🍿': "pop",
	'📤': "pop_out",
	'🎤': "print_top",
	'📥': "push",
	'🔪': "sub",
	'🌓': "xor",
	'⛰': "jump_top",
	'⌛': "exit",
	'✋': "stop",
	'🥇': "accumulator_one",
	'🥈': "accumulator_two"
	# '⃣': ""
}

def main():
	if (len (sys.argv) != 2):
		print('missing something')
		raise SystemExit()

	parser = argparse.ArgumentParser()
	parser.add_argument("input")
	args = parser.parse_args()

	with open(args.input, "r") as f:
		# print(f.read())
		
		lines = f.readlines()
		updated_lines = []
		for i in lines:
			line = list(i.rstrip())
			for j in range(len(line)):
				if line[j] in OPERATIONS:
					line[j] = OPERATIONS [ line[j] ]
					if isinstance(line[j], int):
						print(line[j])
			new_line = " ".join(line)
			updated_lines.append(new_line)

		# print(lines)

		numbers = []
		for i in updated_lines:
			line = i.split(" ")
			# print(line)
			num = []
			for j in line:
				try:
					temp = int(j)
					num.append(str(temp))
				except:
					continue
			# print(num)
			if len(num) >= 2:
				numbers.append("".join(num))
			# 	if isinstance(j, int):
			# 		print(j)


		with open('out.txt', 'w') as f:
			temp = [] # hard coding this
			for i in numbers:
				if i == '106' or i == '99' or i == '765':
					print(i)
					temp.reverse()
					print(temp)
					for j in temp:
						f.write('%s\n' % j)
					temp = []
				else:
					temp.append(i)

if __name__ == '__main__':
	main()
