# crafting payload
import sys

def encode(readin):
	out = "&"
	for i in readin:
		out+= "#" + str(ord(i)).zfill(7)
	return out

def main():
	readin = sys.argv[1]
	# print(readin)
	print(encode(readin))

if __name__ == "__main__":
	main()