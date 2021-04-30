import numpy as np
import gmpy2

def orthonormal(a):
	a = int(sum( list(map(lambda x: x * x, a)) ))
	# return gmpy2.sqrt(a)
	return a


def gs(v):
	ret = []
	ret.append(v[0])
	for i in range(1, len(v)):
		s = np.array(v[i]).astype('float64')
		for j in range(0, i):
			temp = v[i].dot(ret[j]) 
			temp /= ret[j].dot(ret[j])
			temp = temp * ret[j]
			# print(temp, s)
			s -= temp
		ret.append(s)
		
	return ret



def gr(a):
	# 	Loop
	#    (a) If ||v2|| < ||v1||, swap v1, v2
	#    (b) Compute m = ⌊ v1∙v2 / v1∙v1 ⌋
	#    (c) If m = 0, return v1, v2
	#    (d) v2 = v2 - m*v1
	# Continue Loop
	v1 = a[0]
	v2 = a[1]
	m = -1
	while m!= 0:
		if orthonormal(v1) < orthonormal(v2):
			v1, v2 = v2, v1
		m = v1.dot(v2) // v2.dot(v2)
		print(m)
		v1 -= m * v2
	return v1, v2


def main():
	# 1
	v = np.array([2,6,3])
	w = np.array([1,0,0])
	u = np.array([7,7,2])
	# print(3*(2*v - w).dot(2*u))

	#2 
	v = np.array([4, 6, 2, 5])
	print(gmpy2.sqrt(4*4 + 6*6 + 2*2 + 25))

	#3 
	v1 = np.array([4,1,3,-1])
	v2 = np.array([2,1,-3,4])
	v3 = np.array([1,0,-2,7])
	v4 = np.array([6, 2, 9, -5])

	v = [v1,v2,v3,v4]

	# v = [np.array([1,2,2]), np.array([-1,0,2]), np.array([0,0,1])]
	ret = gs(v)
	print("gram schmidttyyyy ", ret)

	
	# whats a lattice
	a = np.array([
		[6, 2, -3],
		[5,1,4],
		[2,7,1]
	])
	print("lattice solution", np.linalg.det(a))

	# gaussian reduction
	a = np.array([
		[846835985, 9834798552],
		[87502093, 123094980]
	])
	v1, v2 = gr(a)
	print("gaussian reduction", v1.dot(v2))
	


	


if __name__ == '__main__':
	main()