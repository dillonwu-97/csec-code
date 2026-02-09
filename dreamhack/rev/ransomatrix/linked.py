import random
from ctypes import CDLL
import ctypes
from ctypes.util import find_library
import numpy as np
from numpy import matrix
from numpy import linalg
import numpy

MOD = 65413
BLK_SIZE = 49

all_rand_vals = []

def phex(a):
    ret = [hex(i) for i in a]
    print(ret)

def encrypt():
    # f = open('/Users/DillonWu/Desktop/input.txt', 'r').read().strip('\n')
    f = open('/Users/DillonWu/Desktop/size-check.txt', 'r').read().strip('\n')
    arr = []
    for i in f:
        arr.append(ord(i))
    if len(arr) % BLK_SIZE != 0:
        arr = arr + ([0] * (BLK_SIZE - (len(arr) % BLK_SIZE)))
    assert len(arr) % BLK_SIZE == 0
    print(arr)
    # assert 0 not in arr
    pt_arr = arr

    libc = ctypes.cdll.msvcrt
    # libc.srand(ord('A'))
    libc.srand(0xffffff89)
    rand_arr = []
    for i in range(len(pt_arr)):
        rand_val = libc.rand()
        all_rand_vals.append(rand_val)
        rand_arr.append(rand_val % MOD)
        # xor_val = c ^ rand_val 
        
    xor_arr = [rand_arr[i] ^ pt_arr[i] for i in range(len(pt_arr))]

    def matrix_mult(a, b):
        SZ = BLK_SIZE // 7
        # capture the rand values
        ret = []
        for i in range(BLK_SIZE):
            rand_val = libc.rand()
            all_rand_vals.append(rand_val % MOD)
            ret.append(rand_val)

        # this is doing the matrix multiplication 
        for i in range(SZ):
            for j in range(SZ):
                ret [j + SZ * i] = 0
                for k in range(SZ):
                    ret [j + SZ * i] += (b[j + k * SZ] * a[k + i * SZ]) % MOD
                    ret [j + SZ * i] %= MOD
        # phex(ret)
        return ret

    final_block = []
    for i in range(0, len(xor_arr), BLK_SIZE):
        cur_block = xor_arr[i:i+BLK_SIZE].copy()

        for j in range(i + BLK_SIZE, len(xor_arr), BLK_SIZE):
            a = cur_block
            b = xor_arr[j: j+BLK_SIZE].copy()
            cur_block = matrix_mult(a, b)
            print("a: ", a)
            # print(cur_block)
            # cur_block = np_mat_mul(a, b)
            # assert cur_block_check == cur_block 
            # print(cur_block)
            # input()

            # phex(a)
            # phex(b)
            # phex(cur_block)
        # phex(cur_block)

        assert len(cur_block) == BLK_SIZE
        print("cur block: ", cur_block)
        for j in range(BLK_SIZE):
            a = cur_block[j] & 0xff
            rand_v = libc.rand()
            all_rand_vals.append(rand_v)
            a ^= rand_v
            a &= 0xff
            b = cur_block[j] >> 8 

            rand_v = libc.rand()
            all_rand_vals.append(rand_v)
            b ^= rand_v
            b &= 0xff
            final_block.append(a)
            final_block.append(b)
        # print("what is this")
        # phex(final_block)
    # print("final block: ")
    # print(len(final_block), hex(len(final_block)))
    # phex(final_block)

    f = open('./test.enc', 'wb')
    to_write = b''
    for i in final_block:
        to_write += i.to_bytes(1, 'big')
    f.write(to_write)
    f.close()

def decrypt():
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

    def invMod(a,mod):
        if a==0:
            return 0
        for i in range(1,mod):
            if(a*i%mod==1):
                return i    
        return 0


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

    def rev_mat_mul(a, d, p):
        '''
        param
        a: matrix list 
        d: (7,7) matrix 
        p: mod val 
        returns b (7,7) matrix 
        '''
        a_inv = inv_matrix(a, p)
        b = np.matmul(a_inv, d)
        return b

    def wrap_rev_mat_mul(a, d, p):
        # do i need to apply transform to a? i think i do 
        # because in forward direction, a gets transformed, and when we store the value back, it is transformed and stored
        for i in range(BLK_SIZE):
            rand_gen.give() 
        
        d = np.reshape(d, (7,7))
        d = d.T
        a = np.reshape(a, (7,7))
        a = a.T.tolist()
        b = rev_mat_mul(a, d, p)
        b = np.mod(b, p)
        return b.T.flatten().tolist()         

    class Rand:
        def __init__ (self):
            self.rand_ctr = 0
            rand_vals = open('./rand_output.txt', 'r').read().split('\n')
            self.rand_vals = [int(i) for i in rand_vals if i != ''][::-1]

        def give(self):
            ret_val = self.rand_vals[self.rand_ctr]
            self.rand_ctr += 1
            return ret_val 

    # Setup 
    # f = open('./test.enc', 'rb').read()[::-1]
    f = open('./FLAG.PNG.enc', 'rb').read()[::-1]
    blocks = []
    for i in range(0, len(f), BLK_SIZE * 2):
        blocks.append(f[i:i+BLK_SIZE * 2]) # reversed 

    rand_gen = Rand()

    rev_blocks = []
    for i,v in enumerate(blocks):
        print(f"i: {i}")
        cur_block = []
        for j in range(0, len(v), 2):
            b = v[j]
            r = rand_gen.give()
            b ^= r
            b &= 0xff

            a = v[j+1]
            r = rand_gen.give()
            a ^= r
            a &= 0xff

            c = a | (b << 8)
            cur_block.append(c)
        
        cur_block = cur_block[::-1]
        cur_rev_mat = cur_block
        print("rev block: ", cur_block)
        for j in range(len(rev_blocks)):
            print(f"j: {j}")
            # a = rev_blocks[ cur pos ], d = cur_rev_mat 
            # what do I get back / do I need to apply transforms to it?
            # yes, i need to apply transforms to it to recover the original value
            print(j)
            cur_rev_mat = wrap_rev_mat_mul(rev_blocks[j], cur_rev_mat, MOD)
            print("a rev: ", cur_rev_mat)
            
        rev_blocks = rev_blocks + [cur_rev_mat] 

    print("rev blocks: ", rev_blocks)
    flag = []
    for i,v in enumerate(rev_blocks):
        cur_block = v[::-1]
        orig_block = []
        for j in cur_block:
            val = j ^ rand_gen.give()
            orig_block.append(val & 0xff)
        print("original: ", orig_block)
        flag = [orig_block[::-1]] + flag
    flag = np.array(flag).flatten().tolist()
    f = open('./flag.png', 'wb')
    to_write = b''
    for i in flag:
        to_write += i.to_bytes(1, 'big')
    f.write(to_write)
    f.close()


def np_mat_mul(a, b):
    assert len(a) == BLK_SIZE and len(b) == BLK_SIZE
    a1 = np.array(a)
    b1 = np.array(b)
    a1 = np.reshape(a1, (7,7)).T
    b1 = np.reshape(b1, (7,7)).T
    c = np.matmul(b1, a1) # reverses this 
    d = np.mod(c, MOD) # reverses this 
    d = d.T
    return d.flatten().tolist()

def generate_rand_list():
    f = open("rand_output.txt", 'w')
    for i in all_rand_vals:
        f.write(str(i) + '\n')
    f.close()

def main():
    # triple_for_loop()
    # get_rand_vals()
    encrypt()
    generate_rand_list()
    

    decrypt()
if __name__ == '__main__':
    main()
    # flag: DH{0x89_is_-119_1n_ch@r6c7er}

