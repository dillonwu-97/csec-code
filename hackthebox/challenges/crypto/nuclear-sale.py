# from scapy.all import *
from collections import Counter




def main():
	
	
	# data = "challenge.pcap"
	# a = rdpcap(data)
	# sessions = a.sessions()
	# print ("Directory fields are: ")

	# d = ''
	# for s in sessions:
	# 	for packet in sessions[s]:
	# 		if len(d) == 0:
	# 			d = dir(packet)
	# 		print(packet[TCP])

	c1 = '6b65813f4fe991efe2042f79988a3b2f2559d358e55f2fa373e53b1965b5bb2b175cf039'
	c2 = 'fd034c32294bfa6ab44a28892e75c4f24d8e71b41cfb9a81a634b90e6238443a813a3d34'
	c3 = 'de328f76159108f7653a5883decb8dec06b0fd9bc8d0dd7dade1f04836b8a07da20bfe70'

	c1a = []
	c2a = []
	c3a = []
	# p1 xor p2 = c1 xor c2
	for i in range(0,len(c1),2):
		# print(c1[i:i+2], int(c1[i:i+2], 16))
		c1a.append(int(c1[i:i+2],16))
		c2a.append(int(c2[i:i+2],16))
		c3a.append(int(c3[i:i+2],16))
	
	# Attack:
	# c1 = sk x p
	# c2 = sk x mk x p
	# c3 = sk x mk x sk x p
	# c3 = mk x p
	# c3 x c2 = mk x p x mk x p x sk
	# c1 x sk = p


	p1p2 = []
	p1p2s = ''

	p1p3 = []
	p1p3s = ''

	p2p3 = []
	p2p3s = ''
	for i in range(len(c1a)):
		temp = c1a[i] ^ c2a[i]
		p1p2.append( temp )
		# p1p2s += chr(temp)

		temp2 = c1a[i] ^ c3a[i]
		p1p3.append( temp2 )
		# p1p3s 

		temp3 = c2a[i] ^ c3a[i]
		p2p3.append( temp3 )

	# print(d)

	ret = []
	for i in range(len(p2p3)):
		ret.append(p2p3[i] ^ c1a[i])

	s = ''.join(chr(i) for i in ret)
	print(s)





if __name__ == '__main__':
	main()
	# HTB{s3cr3t_sh4r1ng_w1th_x0r_15_l4m3}

