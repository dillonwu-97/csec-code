import os
import random
from z3 import *


# System Random from https://github.com/python/cpython/blob/main/Lib/random.py
# https://www.schutzwerk.com/en/43/posts/attacking_a_random_number_generator/
# https://github.com/python/cpython/blob/3.8/Modules/_randommodule.c
# https://stackoverflow.com/questions/41998399/how-exactly-does-random-random-work-in-python
# https://www.youtube.com/watch?v=Jo5Nlbqd-Vg&ab_channel=KringleCon
##### Actual solution involves Mersenne Twister ####
def temper(y):
	y = y^ (y >> 11)
	y = y^ (y << 7) & 0x9d2c5680
	y = y^ (y << 15) & 0xefc60000
	y = y^ (y >> 18)
	return y

def reverse_temper(y):

	# Need to reverse this:
	# Step 1: y = mt[self->index++];
	# 2: y ^= (y >> 11);
	# 3: y ^= (y << 7) & 0x9d2c5680U;
	# 4: y ^= (y << 15) & 0xefc60000U;
	# 5: y ^= (y >> 18);

	# Reversing step 5 first
	# [--- abc (14 bits)---][--- d(4 bits) ---] [--- e (14 bits)---]
	# [--- 0s (18 bits) ----------------------] [---abc(14 bits)---]
	# ________________________________________________________________________
	# [---return val (32 bits)---]

	# abcd = bin(y ^ 0)[2:][:18]
	# abc = abcd[:14]
	# zabc = "0" * 18 + abc
	# x = int(zabc, 2)
	# y4 = y ^ x
	# print(y4)
	print(type(y))
	# Turns out & cannot be reversed and need to use a sat solver
	y0 = BitVec("y0", 32)
	y1 = BitVec("y1", 32)
	y2 = BitVec("y2", 32)
	y3 = BitVec("y3", 32)
	y4 = BitVec(y, 32)
	equations = [
		y1 == y0 ^ (LShR(y0, 11)),
		y2 == y1 ^ ((y1 << 7) & 0x9d2c5680),
		y3 == y2 ^ ((y2 << 15) & 0xefc60000),
		y == y3 ^ (LShR(y3,18))
	]
	s = Solver()
	s.reset()
	s.add(equations)
	s.check()
	ret = s.model()[y0]
	print("ret is ", ret)
	return ret


# linear feedback shift register function
def linear_shift(a):
	# int kk;

	# for (kk=0;kk<N-M;kk++) {
	#     y = (mt[kk]&UPPER_MASK)|(mt[kk+1]&LOWER_MASK);
	#     mt[kk] = mt[kk+M] ^ (y >> 1) ^ mag01[y & 0x1U];
	# }
	# for (;kk<N-1;kk++) {
	#     y = (mt[kk]&UPPER_MASK)|(mt[kk+1]&LOWER_MASK);
	#     mt[kk] = mt[kk+(M-N)] ^ (y >> 1) ^ mag01[y & 0x1U];
	# }
	# y = (mt[N-1]&UPPER_MASK)|(mt[0]&LOWER_MASK);
	# mt[N-1] = mt[M-1] ^ (y >> 1) ^ mag01[y & 0x1U];

	# self->index = 0;
	N = 624
	M = 397
	UPPER_MASK = 0x80000000
	LOWER_MASK = 0x7fffffff
	mag01 = [0x0, 0x9908b0df]
	i = 0
	while i < N-M:
		y = (a[i] & UPPER_MASK) | (a[i + 1] & LOWER_MASK)
		a[i] = a[i + M] ^ (y >> 1) ^ mag01[ y & 1]
		i+=1

	while i < N-1:
		y = (a[i] & UPPER_MASK) | (a[i+1] & LOWER_MASK)
		a[i] = a[i + (M-N)] ^ (y>>1) ^ mag01[y & 1]
		i+=1
	y = (a[N-1] & UPPER_MASK) | (a[0] & LOWER_MASK)
	a[N-1] = a[M-1] ^ (y>> 1) ^ mag01[y & 1]
	return a


def main():
	f = open('./robo_numbers_list.txt', 'r').read()
	rnumbers = f.split("\n")
	rnumbers = [i.replace("-","") for i in rnumbers]
	rnumbers = [str(int(i) - (1<<31)) for i in rnumbers]

	# a = [reverse_temper(i) for i in rnumbers]
	a = [3244477332, 268925762, 1331042339, 2965566132, 1668631255, 2961729969, 4029593717, 3859274707, 3056896947, 1935429209, 2145532196, 894015853, 3720928345, 3345181890, 2733247249, 1642080068, 3617645783, 797066199, 3901536060, 2422178836, 945863016, 1974915130, 3367065220, 641343419, 3584464947, 2497325999, 4132151237, 1273451449, 208698566, 2158613942, 3132070328, 4067593776, 274826293, 1685647538, 3026932233, 2933177622, 174478927, 2205166943, 4194523114, 1601030673, 3180764689, 2650905952, 1742779143, 2893438257, 616436361, 2008492297, 3635086785, 1989131153, 2380140467, 252988094, 666654419, 4145377772, 3170928723, 2780391544, 1064483219, 478862623, 2768607860, 4004266663, 2994549374, 3980425761, 228422873, 3150936955, 3750237426, 1281195522, 345127999, 3607850537, 1888526036, 342885276, 2412379122, 2485045736, 3373383168, 1973900593, 1488953778, 1799945329, 4004873718, 4004250749, 1477480931, 46482399, 4041102718, 3651395969, 945143976, 121114632, 1943143756, 3625352388, 4157075736, 2871650338, 866723650, 1128391485, 3874588699, 1655651386, 2805266901, 4287909004, 298221129, 3170871589, 4214729450, 682271467, 3321818983, 2284640214, 465829082, 2237980073, 5743072, 1921155440, 679429482, 4144220601, 2606632415, 1035435260, 1009229508, 1866190715, 707154995, 1691349322, 1620297398, 2780030652, 317044845, 825618695, 646895567, 1158967835, 1971232131, 2092465183, 1566691969, 1836042227, 3357402277, 4254975845, 3639047180, 4063976237, 2233630183, 170255408, 4117132936, 3169668512, 3459154159, 1124793648, 4232706680, 3604406548, 1466085773, 2953197811, 2169321848, 1013555701, 3634810002, 285730443, 1850699685, 2138458378, 3056753709, 2211618530, 363386539, 1036150837, 671844, 3711769859, 140265782, 1638253548, 734708710, 1689592161, 1975922255, 4092626455, 3712638144, 43222293, 223295765, 3158926159, 3528649710, 3961093091, 353117828, 119666178, 3161665177, 511062113, 4177825397, 1973986366, 1311192444, 2161541716, 4263980329, 3057004423, 2866837029, 3382967780, 2158559776, 919822242, 1470886987, 2162793812, 2151336254, 3198689862, 1280184740, 1165656897, 4077390754, 3937391507, 2161282207, 2453331990, 189009817, 2321036697, 2581289061, 4045426324, 1441598569, 2337120527, 2725027976, 3565552290, 3900028082, 4192939918, 1242385846, 556684811, 3150140207, 1977930556, 2270932210, 869314849, 2647786924, 3055661477, 2157158982, 3299323340, 3934846680, 2684337009, 3751751829, 3545443004, 2357040074, 2154483869, 1523638000, 3484629279, 2335526612, 951857825, 917864080, 557759720, 3859891351, 306190940, 4261920770, 2036348636, 3868602953, 4206257575, 1091899882, 12226892, 403140216, 3448630949, 1576011628, 1011479532, 1228571452, 71718424, 1177503723, 3654754280, 2638916540, 3765384748, 1840031997, 3990045247, 3879015147, 3875481518, 2553623148, 2568896245, 998392191, 2165573013, 2749496267, 468842974, 405906943, 1113429513, 3390785632, 3764318673, 1190458693, 4082575111, 677219575, 3455803494, 55687905, 1872803414, 1053887039, 1536396574, 2224420801, 4180177546, 3849602837, 74639351, 1163197286, 1492417581, 3847792772, 1292576682, 702564330, 1104907213, 3613754071, 587750676, 2191463422, 204851742, 3254717041, 34840831, 2826888331, 1178638917, 212175442, 1562668522, 3155204328, 3320394820, 4113622925, 2043193728, 400438609, 1978742083, 3318592114, 2053322414, 53575239, 621952119, 3785404290, 124630803, 2195822620, 424604614, 790335231, 1937914967, 797161395, 4096680177, 3233884915, 3735348466, 1828544033, 4148903175, 2475730348, 321758268, 3302693981, 2328791666, 2095708030, 1837764082, 2756923543, 4001961394, 3664359940, 3202986929, 2126406043, 1312344451, 20361765, 410121174, 614751517, 1721772431, 125135393, 1849337211, 2845104574, 3169382737, 4181842535, 2148215637, 1405376638, 2265763219, 3373118644, 2562810376, 1158402773, 1236480823, 3604787333, 2291572821, 3302122785, 455448980, 2129402303, 3519991601, 3070709684, 1117435639, 2570125075, 733470617, 2544752034, 90656383, 4266893736, 1138432335, 2014981802, 2766853416, 729133751, 2339966687, 28199592, 1902775062, 3028967752, 1707057704, 2532589022, 1619185294, 3972876995, 1422497914, 383731912, 2605120049, 4111707463, 3564402893, 3626928079, 1884499693, 2310970192, 1143385694, 3928874101, 460168325, 1785548768, 1280610417, 3047485915, 3233147352, 2907881915, 1607170700, 967421765, 4084409565, 789845764, 920951505, 2856300205, 1515880497, 3910491043, 504618148, 2525234425, 3632527774, 3622967174, 3868321576, 4083711969, 2798983554, 2583944338, 3713995810, 1536666957, 2795618250, 3151327906, 2742995993, 3041183349, 2493917464, 3883558305, 3859630492, 3364500227, 1839813473, 1534974924, 1626656350, 3383107619, 3978266777, 2462391694, 7994409, 3663695018, 67903023, 3865824779, 3287979434, 1351849256, 2552924378, 2259729695, 3319002688, 3832942204, 233710029, 3526829107, 885159768, 933345234, 2040061673, 1368233556, 3321128658, 515220388, 3234111792, 2716964855, 1971158905, 1472887353, 1893632717, 50380723, 3695577481, 390115774, 1847542740, 1633691526, 2470221728, 2644381203, 629443413, 102160829, 3570572731, 3910175006, 2674833949, 2240908797, 2796875489, 2793818257, 2748351047, 2644980341, 2765639866, 1582259755, 2424285140, 220125348, 399830380, 558520483, 3670761546, 4273034300, 3579055200, 3005404201, 2388814675, 3609721254, 1639461263, 3131415172, 727372656, 4161800493, 2987126290, 2195463905, 3952704624, 3751431816, 2201376759, 1448668440, 3582406333, 157220457, 2559263788, 3698567033, 3803569555, 2149545641, 3906766663, 4043871488, 3298765827, 4208357222, 2062050643, 763292825, 3625984991, 3590488775, 2637570933, 2215155217, 2811157560, 458397953, 356674435, 3215210323, 3986775290, 815857322, 572130415, 3688122157, 1321057946, 3504264511, 4214084353, 518199118, 2544295361, 1354605717, 1820023180, 2623898757, 291556395, 1164154416, 1626270690, 1646111195, 1934348169, 1799174584, 2289747456, 1066651327, 1572792637, 3204510789, 3650298387, 1100071566, 253958366, 4172288168, 3147512120, 3193843192, 2794947863, 1724800670, 2611059471, 2301694646, 2970790898, 2045162999, 1345581127, 4030384314, 3306733209, 2869748037, 3150221119, 4075627356, 1510703618, 2192505771, 3448111426, 36128415, 2671497231, 2234995115, 4040864219, 1044940625, 3665225451, 1273014346, 3809562901, 774954489, 3165324939, 194738095, 1962112257, 3345422986, 48439121, 2613693267, 288131559, 1176169247, 2582049973, 2318743894, 1586938875, 1154762549, 1083461967, 3400503734, 2913164367, 250366460, 1970104435, 83457245, 1678327438, 2193627927, 2753936435, 1338808287, 2072893623, 3502793618, 3849750894, 3638243847, 3741558072, 1762747173, 4056354291, 2129599664, 2325188755, 3775074111, 2077403655, 1391761587, 3844770488, 778489668, 67584112, 2489691285, 3917072566, 4003937013, 1404997605, 1596384491, 722955628, 1453565989, 558221499, 2428413628, 131173256, 1922066610, 4139848315, 1680927147, 3800667212, 2168362262, 211452152, 193362144, 174813006, 1463107843, 1814449570, 1233155987, 3516950118, 3488155557, 3919721915, 4106686872, 1573182426, 2731314187, 3495121593, 3296393518, 135280551, 1415263346, 2084600012, 2070974747, 3931720408, 2206051006, 3894743167, 3476958823, 3025934750, 2478835789, 675765107, 346368693, 2681891778, 2322521946, 3230673069, 1245152237, 2236198520, 633139088, 3616230125, 305668097, 4025164499, 2498525396, 90489647, 2246207703, 3045801759, 1000952793, 2993977412]
	# print(a)
	a = linear_shift(a)

	s = open('./secret.enc', 'rb').read()
	key = [int(bin(temper(a[i]))[2:].zfill(32)[:8],2) for i in range(len(s))]
	s_array = [int(hex(k),16) for k in s]
	val = bytes([a^b for a,b in zip(key,s_array)])
	print(val)
	# Flag: CTF{n3v3r_3ver_ev3r_use_r4nd0m}




if __name__ == '__main__':
	main()

##### Tried exploiting random seed generated according to current time #####
# R = './RoboCaller1337.py'
# S = './secret.enc'
# N = './robo_numbers_list.txt'

# print("python script ", os.stat(R))
# print("secret enc ", os.stat(S))
# print("robo numbers list ", os.stat(N))

# start = min(os.path.getctime(R), os.path.getctime(S), os.path.getctime(N))
# print(start)

# for i in range(int(start)-100000,1640960000):
# 	random.seed(a = i)
# 	# state = random.getstate()
# 	# random.setstate(state)
# 	s = open('./secret.enc', 'rb').read()
# 	key = [random.getrandbits(8) for k in range(len(s))]
# 	s_array = [int(hex(k),16) for k in s]
# 	assert(len(key) == len(s_array))
# 	val = bytes([a^b for a,b in zip(key,s)])
# 	print(i, val)
# 	if b'CTF{' in val:
# 		print("found ", val)
# 		break


##### Tried matching with robo numbers list #####
# f = open('./secret.enc', 'rb').read()
# s = f.hex()
# a = [s[i:i+1] for i in range(0,len(s), 2)]


# f2 = open('./robo_numbers_list.txt', 'r').read()
# rnumbers = f2.split("\n")
# rnumbers = [i.replace("-","") for i in rnumbers]
# print(rnumbers)
# rnumbers = [int(i) - (1<<31) for i in rnumbers]


# br = [bin(i) for i in rnumbers]

# start = ["C", "T", "F", "{"]
# to_search = []
# for i in range(len(start)):
# 	to_search.append(ord(start[i]) ^ int(a[i],16))

# to_search = [bin(i)[2:] for i in to_search]
# print(to_search)

# temp = []
# for i in range(len(to_search)):
# 	print("-"* 50)
# 	for j in range(len(br)):
# 		if to_search[i] in br[j]:
# 			print("found something!", i, j)
# 			temp.append((j, i))
# temp.sort( key=lambda x: x[0])
# for i in range(len(temp)-4):

# 	if temp[i][1] == 0:
# 		if temp[i+1][1] == 1:
# 			if temp[i+1][1] == 2:
# 				# if temp[i+1][0] == 3:
# 				print("FOUND")
# 				print(i)



