from Crypto.Util.number import *
import gmpy2
import itertools

def sage_solve():

    gmpy2.get_context().precision=int(10000)
    k = '''
000bfdc32162934ad6a054b4b3db8578674e27a165113f8ed018cbe9112
4fbd63144ab6923d107eee2bc0712fcbdb50d96fdf04dd1ba1b69cb1efe
71af7ca08ddc7cc2d3dfb9080ae56861d952e8d5ec0ba0d3dfdf2d12764
'''.replace('\n', '')
    k = int(k, 16) * 4

    # print(int(k, 16))
    # var('x y z')

    #f = (x^2 + 1)*(y^2 + 1) - 2*(x - y)*(x*y - 1) - 4*x*y
    # z = factor(f)
    # print(z)
    # print(factor(k))

    #keq = 2^4 * 3^2 * 11^4 * 19^2 * 47^2 * 71^2 * 3449^2 * 11953^2 * 5485619^2 * 2035395403834744453^2 * 17258104558019725087^2 * 1357459302115148222329561139218955500171643099^2
    kfac = [2,3,11,19,47,71,3449,11953,5485619, 2035395403834744453, 17258104558019725087,1357459302115148222329561139218955500171643099]
    kexp = [4,2,4,2,2,2,2,2,2,2,2,2]
    
    sq = int(gmpy2.sqrt(k))
    sage_factors = factor(sq)
    factors = []
    for i in sage_factors:
        for j in range(i[1]):
            factors.append(i[0])
    indices = [i for i in range(len(factors))]
    
    all_comb = []
    for i in range(1,len(factors)):
        comb = itertools.combinations(factors,i)
        all_comb += comb
    for i in all_comb:
        print(i)
    for i in all_comb:
        print(i)
        if b'CCTF' in long_to_bytes(prod(i)-1):
            print(long_to_bytes(prod(i) - 1))
            print(long_to_bytes(sq // prod(i) + 1))
            print("Found!:")
            input()
    # flag: b'CCTF{S1mPL3_4Nd_N!cE_Diophantine_EqUa7I0nS!}'

    
    

def sandbox():
    n = 64
    for i in factor(n):
        print(i)

def main():
    sage_solve()
    #sandbox()

if __name__ == '__main__':
    main()
