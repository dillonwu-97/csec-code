from sympy import *
from hashlib import md5
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from random import randint, randbytes,seed
from Crypto.Util.number import bytes_to_long

FLAG = b'HTB{dummyflag}'
class Shamir:

    # need k shares to reconstruct the secret
    # n is total number of shares to create
    def __init__(self, prime, k, n):
        self.p = prime
        self.secret = randint(1,self.p-1) # how to recover the secret value?
        self.k = k
        self.n = n
        self.coeffs = [self.secret]
        self.x_vals = []
        self.y_vals = []

    def next_coeff(self, val):
        return int(md5(val.to_bytes(32, byteorder="big")).hexdigest(),16)

    def calc_coeffs(self):
        # repeatedly calculate the md5 hash integerized and use it as the source of the next coefficient
        # so basically the next coefficient is randomized and there is no leak?
        for i in range(1,self.n+1):
            self.coeffs.append(self.next_coeff(self.coeffs[i-1]))

    def calc_y(self, x):
        y = 0
        # iteration is k times
        for i, coeff in enumerate(self.coeffs):        
            y +=coeff *x**i
        return y%self.p

    # create the polynomials
    def create_pol(self):
        self.calc_coeffs()
        self.coeffs = self.coeffs[:self.k] # we get rid of some of the coefficients at this point, but to what end?
        # we get rid of some of the coefficients because the coeff array is used in the calculation of y vals?
        # x is a random value so there is no way to recover x??? How can I use the share that was disclosed
        for i in range(self.n):
            x = randint(1,self.p-1)
            self.x_vals.append(x) # iteratively get x
            self.y_vals.append(self.calc_y(x)) # iteratively get y

    def get_share(self):
        return self.x_vals[0], self.y_vals[0]


def main():
    sss = Shamir(92434467187580489687, 10, 18) # shamir secret sharing
    sss.create_pol()
    share = sss.get_share()
    seed(sss.secret)
    key = randbytes(16)
    cipher = AES.new(key, AES.MODE_ECB)
    enc_FLAG = cipher.encrypt(pad(FLAG,16)).hex()
    
    f = open('msg.enc', 'w')
    f.write('share: ' + str(share) + '\n')
    f.write('coefficient: ' + str(sss.coeffs[1]) + '\n')
    f.write('secret message: ' + str(enc_FLAG) + '\n')
    f.close()

if __name__ == "__main__":
    main()


