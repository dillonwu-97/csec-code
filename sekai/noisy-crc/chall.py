import secrets
from Crypto.Util.number import *
from Crypto.Cipher import AES
from hashlib import sha256

#from flag import FLAG
FLAG = b'hello world'

# cyclic reundancy checking of value = 16
# idea for this is to leak 1 bit at a time
# i can try to solve for easier case first, i.e. case without the noise added
# Always going to be flipping the first bits
# not really sure how we are recovering information 
def getCRC16(msg, gen_poly):
	# generator polynomial is a large number
	assert (1 << 16) <= gen_poly < (1 << 17)  # check if deg = 16
	msglen = msg.bit_length()

	msg <<= 16
	# for each  
	for i in range(msglen - 1, -1, -1):
		# print(f"i: {i}, msg: {bin(msg)[2:]}")

		# So to summarize: if the current bit is flipped, convert it to 0?
		# if the current bit is flipped
		if (msg >> (i + 16)) & 1:
			print(i+16)
			# perform an xor operation with the value that we passed in
			# so basically flip the bit 
			# print(f"i: {i}, msg: {bin(msg)[2:].zfill(528)}")
			msg ^= (gen_poly << i)
			# print(f"i: {i}, msg: {bin(msg)[2:].zfill(528)}")
			input()

	return msg

def oracle(secret, gen_poly):
	# res = [secrets.randbits(16) for _ in range(3)] 
	# res[secrets.randbelow(3)] = getCRC16(secret, gen_poly)
	
	# return res
	return getCRC16(secret, gen_poly)


# lattice attack maybe?
# 
def main():
	# key = secrets.randbits(512)
	temp = '10' * 256
	key = int(temp, 2)
	print(key)

	# can the nonce just be anything? i think in ctr mode, the nonce is used to initialize some start value so this might be dangerous
	# the goal here seems to be that we need to recover the key somehow
	cipher = AES.new(sha256(long_to_bytes(key)).digest()[:16], AES.MODE_CTR, nonce=b"12345678")


	enc_flag = cipher.encrypt(FLAG)
	print(f"Encrypted flag: {enc_flag.hex()}")

	used = set({})

	# i think i can send as many generator polynomials as i would like
	while True:
		#gen_poly = int(input("Give me your generator polynomial: "))
		gen_poly = (1<<17)-1
		print(bin(gen_poly))
		assert (1 << 16) <= gen_poly < (1 << 17)  # check if deg = 16
        

		# cannot reuse generator polynomials
		if gen_poly in used:
			print("No cheating")
			exit(1)

		used.add(gen_poly)

		# leak some information about the key given the generator polynomial?
		print(oracle(key, gen_poly))
		input()

main()
