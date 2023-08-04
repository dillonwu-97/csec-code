from pwn import *
from base64 import *
from requests import *
from hashlib import md5
from random import randint, seed, randbytes
from Crypto.Util.number import bytes_to_long, long_to_bytes
from Crypto.Cipher import AES

class Shamir:

    # need k shares to reconstruct the secret
    # n is total number of shares to create
    def __init__(self, prime, k, n):
        self.p = prime
        self.secret = randint(1,self.p-1) # how to recover the secret value (even if i knew all of the coefficients)
        self.k = k
        self.n = n
        self.coeffs = [self.secret]
        self.x_vals = []
        self.y_vals = []

    def next_coeff(self, val):
        return int(md5(val.to_bytes(32, byteorder="big")).hexdigest(),16)

    def calc_coeffs(self):
        # repeatedly calculate the md5 hash integerized and use it as the source of the next coefficient
        for i in range(1,self.n+1):
            self.coeffs.append(self.next_coeff(self.coeffs[i-1]))

    def calc_y(self, x):
        y = 0
        for i, coeff in enumerate(self.coeffs):        
            y +=coeff *x**i
        return y%self.p

    # create the polynomials
    def create_pol(self):
        self.calc_coeffs()
        self.coeffs = self.coeffs[:self.k]
        for i in range(self.n):
            x = randint(1,self.p-1)
            self.x_vals.append(x)
            self.y_vals.append(self.calc_y(x))

    def get_share(self):
        return self.x_vals[0], self.y_vals[0]

'''
Steps: 
1) Find the k coefficients
2) Using x0, keep on calculating the k values
'''
def solve():
    share = (21202245407317581090, 11086299714260406068)
    coef = 93526756371754197321930622219489764824 # this is an md5 hash of the sss secret
    cipher = '1aaad05f3f187bcbb3fb5c9e233ea339082062fc10a59604d96bcc38d0af92cd842ad7301b5b72bd5378265dae0bc1c1e9f09a90c97b35cfadbcfe259021ce495e9b91d29f563ae7d49b66296f15e7999c9e547fac6f1a2ee682579143da511475ea791d24b5df6affb33147d57718eaa5b1b578230d97f395c458fc2c9c36525db1ba7b1097ad8f5df079994b383b32695ed9a372ea9a0eb1c6c18b3d3d43bd2db598667ef4f80845424d6c75abc88b59ef7c119d505cd696ed01c65f374a0df3f331d7347052faab63f76f587400b6a6f8b718df1db9cebe46a4ec6529bc226627d39baca7716a4c11be6f884c371b08d87c9e432af58c030382b737b9bb63045268a18455b9f1c4011a984a818a5427231320ee7eca39bdfe175333341b7c'
    x0 = share[0]
    y0 = share[1]
    c = [None,coef] # add a null value just for simplicity
    p = 92434467187580489687

    def get_next_coeff(val):
        return int(md5(val.to_bytes(32, byteorder="big")).hexdigest(),16)
    
    k: int = 10 # need 10 to recover the polynomial
    n: int = 18 # divided into 18 partitions
    
    # Getting the k-2 coefficients needed
    # [secret, coeff[1], ...k-2 rest of the coefficients]
    # Including the coefficient we are given, we will have all of coefficients we need except the very first one which is out secret value
    for i in range(1, k-1):
        new_coef = get_next_coeff(c[i])
        c.append(new_coef)

    assert(len(c) == k)

    y = 0 # Will eventually use this and y0 to get the secret

    for i in range(1,len(c)):
        y += (x0 ** i) * c[i]

    yp = y % p
    ydiff = yp - y0
    # y -= ydiff
    secret = -ydiff % p

    print(get_next_coeff(secret), c[i])

    print(y, (y + secret) % p, y0)
    assert(secret <= p)
    assert ((y + secret) % p == y0)
    assert(get_next_coeff(secret) == c[1])

    seed(secret)
    key = randbytes(16)
    cipher = AES.new(key, AES.MODE_ECB)
    c = '1aaad05f3f187bcbb3fb5c9e233ea339082062fc10a59604d96bcc38d0af92cd842ad7301b5b72bd5378265dae0bc1c1e9f09a90c97b35cfadbcfe259021ce495e9b91d29f563ae7d49b66296f15e7999c9e547fac6f1a2ee682579143da511475ea791d24b5df6affb33147d57718eaa5b1b578230d97f395c458fc2c9c36525db1ba7b1097ad8f5df079994b383b32695ed9a372ea9a0eb1c6c18b3d3d43bd2db598667ef4f80845424d6c75abc88b59ef7c119d505cd696ed01c65f374a0df3f331d7347052faab63f76f587400b6a6f8b718df1db9cebe46a4ec6529bc226627d39baca7716a4c11be6f884c371b08d87c9e432af58c030382b737b9bb63045268a18455b9f1c4011a984a818a5427231320ee7eca39bdfe175333341b7c'
    ret = cipher.decrypt(bytes.fromhex(c))
    print(ret)

    # Flag: HTB{1_d1dnt_kn0w_0n3_sh4r3_w45_3n0u9h!1337}



def main():
    print("[*] Starting solve")
    solve()

if __name__ == '__main__':
    main()


