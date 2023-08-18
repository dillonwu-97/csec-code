from Crypto.Util.number import getPrime, long_to_bytes, inverse
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from hashlib import sha256
from secret import FLAG


class RNG:

    def __init__(self, seed):
        self.e = 0x10001
        self.s = seed

        self.r = getPrime(768)
        while True:

            # self.p < self.r, self.q < self.r <-- upper bound on the prime r
            # this also seems somewhat relevant? 
            self.p, self.q = getPrime(768), getPrime(768)
            if self.p < self.r and self.q < self.r:
                break

        self.n = self.p * self.q * self.r # n value with three different factors
        phi = (self.p - 1) * (self.q - 1) * (self.r - 1) # calculate phi
        self.d = inverse(self.e, phi) 


    # s5 = (s4 * p + q) % r
    # s4 = (s3 * p + q) % r
    # s5 = (((s3 * p + q) % r) * p + q) % r
    # s3 = (((s1 * p + q) % r) * p + q) % r
    # s2 = (s1 * p + q) % r

    def next(self): 
        self.s = (self.s * self.p + self.q) % self.r # getting the next seed value, which is the initial (seed * p + q) % r
        return self.s

# What is the seed used for?
# The goal is to somehow use the seed values to recover the plaintext
# Maybe I take each of the seeds and use them to recover candidates for p,q,r values?
# It also feels weird that the n value is comprised of three primes but a cursory google search seems to imply that it's not a security issue
def main():
    rng = RNG(getPrime(512)) # random seed
    rns = [rng.next() for _ in range(5)] # five different seeds / random numbers

    key = sha256(long_to_bytes(rng.d)).digest()
    cipher = AES.new(key, AES.MODE_ECB)
    enc_flag = cipher.encrypt(pad(FLAG, 16)).hex()

    with open('output.txt', 'w') as f:
        f.write(f'n = {rng.n}\n') # we have the value for n
        f.write(f's = {rns}\n') # we have next few seed values but not the first one
        f.write(f'enc_flag = {enc_flag}\n')


if __name__ == "__main__":
    main()
