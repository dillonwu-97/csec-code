import math
UMAX = int(math.pow(256, 16))


def remove_line(s):
    # returns the header line, and the rest of the file
    print(type(s))
    return s[:s.index(b'\n') + 1], s[s.index(b'\n')+1:]

def parse_header_ppm(data):

    header = b''

    for i in range(3):
        header_i, data = remove_line(data)
        header += header_i

    return header, data

if __name__ == '__main__':
	with open('body.enc.ppm', 'rb') as f:
		data = f.read()

	# How to find the header of the file?
	header, file = parse_header_ppm(data)	

	chunks = [file[ 16*i : 16*(i+1) ] for i in range(len(file) // 16)]
	for i in range(len(chunks)):
		chunks[i] = int.from_bytes(chunks[i], "big")
	original_message = [0] * (len(file) // 16)

	for i in range(len(chunks)-1, 0, -1):
		original_message[i] = chunks[i] - chunks[i-1]
		original_message[i] %= UMAX

	# converting chunks into AES encrypted data
	for i in range(1, len(original_message)):
		original_message[i] = bytes.fromhex((str(hex(original_message[i]))[2:]).zfill(32))
	ret = b''.join(original_message[1:])
	print(ret)
	with open('temp.enc.ppm', 'wb') as temp:
		temp.write(header)
		temp.write(ret)

	