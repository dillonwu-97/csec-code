import numpy as np
import numpy
from numpy import matrix
from numpy import linalg

MOD = 65413
BLK_SIZE = 49
def invMod(a,mod):
    if a==0:
        return 0
    for i in range(1,mod):
        if(a*i%mod==1):
            return i    
    return 0

def inv_matrix(matrix , mod):
    dim= len(matrix)
    
    idMat=[]
    for i in range(dim):
        row=[]
        for j in range(dim):
            if(i==j):
                row.append(1)
            else:
                row.append(0)

        idMat.append(row)
    
    M = matrix
    for i in range(dim):
        for x in idMat[i]:
            M[i].append(x)

    
    Mcpy= matrix
    ToReducedRowEchelonForm(Mcpy,mod)
    #should be == idMat

    for i in range(dim):
        for j in range(dim):
            if Mcpy[i][j]!= idMat[i][j]:
                raise Exception("Matrix isn't invertible ")
                quit()

    ToReducedRowEchelonForm(M,mod)
    invMat=[]

    for x in range(0,dim):
        row=[]
        for y in range(dim,2*dim):
            row.append(M[x][y])
        
        invMat.append(row)

    return invMat



def ToReducedRowEchelonForm( M,mod):
    if not M: return
    lead = 0
    rowCount = len(M)
    columnCount = len(M[0])
    for r in range(rowCount):
        if lead >= columnCount:
            return
        i = r
        while invMod(M[i][lead],mod) == 0:
            i += 1
            if i == rowCount:
                i = r
                lead += 1
                if columnCount == lead:
                    return
        M[i],M[r] = M[r],M[i]
        lv = M[r][lead]
        
        M[r] = [ mrx * invMod(lv,mod)%mod for mrx in M[r]]
        
        for i in range(rowCount):
            if i != r:
                lv = M[i][lead]
                M[i] = [ (iv - lv*rv)%mod for rv,iv in zip(M[r],M[i])]
        lead += 1

def modMatInv(A,p):       # Finds the inverse of matrix A mod p
  n=len(A)
  A=matrix(A)
  adj=numpy.zeros(shape=(n,n))
  for i in range(0,n):
    for j in range(0,n):
      adj[i][j]=((-1)**(i+j)*int(round(linalg.det(minor(A,j,i)))))%p
  return (modInv(int(round(linalg.det(A))),p)*adj)%p

def modInv(a,p):          # Finds the inverse of a mod p, if it exists
  for i in range(1,p):
    if (i*a)%p==1:
      return i
  raise ValueError(str(a)+" has no inverse mod "+str(p))

def minor(A,i,j):    # Return matrix A with the ith row and jth column deleted
  A=numpy.array(A)
  minor=numpy.zeros(shape=(len(A)-1,len(A)-1))
  p=0
  for s in range(0,len(minor)):
    if p==i:
      p=p+1
    q=0
    for t in range(0,len(minor)):
      if q==j:
        q=q+1
      minor[s][t]=A[p][q]
      q=q+1
    p=p+1
  return minor

def mat_mul(a, b, p):
    c = np.matmul(a, b)
    d = np.mod(c, p)
    return d

def mod_inv_two(a, p):
    A_adj = np.linalg.inv(a) * round(np.linalg.det(a))
    print(A_adj)
    A_inv_det_Z26 = pow(round(np.linalg.det(a)), -1, p)
    print(A_inv_det_Z26)
    A_inv_Z26 = A_inv_det_Z26 * A_adj
    A_inv_Z26 = A_inv_Z26 % p
    print(np.matmul(a, A_inv_Z26)% p)
    a_inv = np.matmul(a, A_inv_Z26) % p
    a_inv = a_inv.astype(int)
    return a_inv

def rev_mat_mul(a, d, p):
    # a_inv = np.mod(modMatInv(a, p), p)
    # print("other: ", a_inv)
    # a_inv = mod_inv_two(a, p)

    a_inv = inv_matrix(a, p)
    print("inv: ", a_inv)
    temp = np.mod(np.matmul(np.matrix(a_inv),np.matrix(a)), p)
    print("temp: ", temp)
    b = np.matmul(a_inv, d)
    print(b)
    # b = np.mod(b, p)
    return b

def wrap_mat_mul(a, b):
    assert len(a) == BLK_SIZE and len(b) == BLK_SIZE
    a1 = np.array(a)
    b1 = np.array(b)
    a1 = np.reshape(a1, (7,7)).T
    b1 = np.reshape(b1, (7,7)).T
    c = np.matmul(b1, a1) # reverses this 
    d = np.mod(c, MOD) # reverses this 

    # Testing 
    # get a1 back, not b1 
    # a1 = np.reshape(a1, (7,7)).tolist()
    # b1 = np.reshape(b1, (7,7)).tolist()
    # print(np.mod(rev_mat_mul(b1, d, MOD), MOD))
    # print(a1)
    # input()
    
    d = d.T
    return d.flatten().tolist()

def wrap_rev_mat_mul(a, d, p):
    # do i need to apply transform to a? i think i do 
    # because in forward direction, a gets transformed, and when we store the value back, it is transformed and stored
    d = np.reshape(d, (7,7))
    d = d.T
    a = np.reshape(a, (7,7))
    a = a.T.tolist()
    b = rev_mat_mul(a, d, p)
    b = np.mod(b, p)
    return b.T.flatten().tolist()         


def main():
    p = 101
    # a = np.matrix([[5,3],[-3,5]])
    a = [[5,3], [-3,5]]
    b = [[1,5], [3,7]]
    # b = np.matrix([[1,5],[3,7]])
    #
    p = 65413
    a = [187, 18300, 2696, 26393, 24007, 4955, 14003, 5789, 2422, 24269, 28942, 30901, 31208, 27153, 21173, 28720, 15475, 11445, 23752, 3622, 9257, 22281, 14514, 23166, 17314, 32081, 4976, 24649, 3845, 13754, 962, 31055, 21556, 19096, 22419, 751, 26226, 17225, 15117, 30505, 8331, 26222, 270, 7799, 11361, 1646, 6089, 17501, 7860]
    #
    print(a)
    a = np.reshape(a, (7,7)).tolist()
    print(a)
    # input()
    b = [9493, 25374, 13379, 26411, 19610, 3780, 24831, 7421, 10042, 1856, 30001, 7714, 13512, 13928, 16483, 9313, 10079, 13154, 10807, 9097, 17718, 29737, 13473, 12176, 23796, 17575, 10166, 13095, 7333, 32662, 28579, 12269, 29013, 22549, 22050, 24088, 10139, 12358, 3836, 23825, 32693, 16525, 18540, 18316, 27941, 7788, 14880, 24778, 10803]
    b = np.reshape(b, (7,7)).tolist()
    #

    d = mat_mul(a, b, p)
    print(d.shape)
    print(d)
    e = rev_mat_mul(a, d, p).astype(int)
    print(e.shape)
    print()
    print()
    print()
    # input()
    print(np.mod(b, p))
    print(np.mod(e, p))
    # print(b)
    # print(e)
    # assert np.allclose(b, e)
    
    print("Testing transform mat mul")

    a = [187, 18300, 2696, 26393, 24007, 4955, 14003, 5789, 2422, 24269, 28942, 30901, 31208, 27153, 21173, 28720, 15475, 11445, 23752, 3622, 9257, 22281, 14514, 23166, 17314, 32081, 4976, 24649, 3845, 13754, 962, 31055, 21556, 19096, 22419, 751, 26226, 17225, 15117, 30505, 8331, 26222, 270, 7799, 11361, 1646, 6089, 17501, 7860]
    # input()
    b = [9493, 25374, 13379, 26411, 19610, 3780, 24831, 7421, 10042, 1856, 30001, 7714, 13512, 13928, 16483, 9313, 10079, 13154, 10807, 9097, 17718, 29737, 13473, 12176, 23796, 17575, 10166, 13095, 7333, 32662, 28579, 12269, 29013, 22549, 22050, 24088, 10139, 12358, 3836, 23825, 32693, 16525, 18540, 18316, 27941, 7788, 14880, 24778, 10803]

    d = wrap_mat_mul(a, b)
    a_ret = wrap_rev_mat_mul(b, d, MOD)

    print(a)
    print(a_ret)
    assert a == a_ret



if __name__ == '__main__':
    main()
