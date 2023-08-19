from Crypto.Util.number import isPrime, long_to_bytes, getPrime
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from random import randint
from hashlib import sha256

from secret import FLAG


# small-subgroup-attack
class DH:

    def __init__(self):
        self.gen_params()

    def gen_params(self):
        # very big
        self.r = getPrime(512)

        # get the p value
        while True:
            # this seems very small
            # i think this might be the vulnerability
            self.q = getPrime(42)
            self.p = (2 * self.q * self.r) + 1
            if isPrime(self.p):
                break

        while True:
            self.h = getPrime(42)

            # dont really understand why the generator is constructed with h^2*r % p
            self.g = pow(self.h, 2 * self.r, self.p)

            # g is 1, so h is of order less than 2 * r, so pick another h and try again?
            # or is it 2 * r * q?
            if self.g != 1:
                break

        # a = random number from 2 -> p-2
        # b = random number from 2 -> p-2
        self.a = randint(2, self.p - 2)
        self.b = randint(2, self.p - 2)

        # A = g^a % p
        # B = g^b % p
        self.A, self.B = pow(self.g, self.a, self.p), pow(self.g, self.b, self.p)

        # ss generated from A^b % p
        # need to recover b somehow which is equivalent to solving the discrete log problem?
        # but things are being reused, so maybe there is some group theory stuff that can be done to recover important values
        # actually, it seems like nothing is being reused
        # across gen_params() calls, nothing is consistent
        self.ss = pow(self.A, self.b, self.p)

    def encrypt(self, flag_part):

        # ss is used for the key so need to recover ss
        key = sha256(long_to_bytes(self.ss)).digest()[:16]
        cipher = AES.new(key, AES.MODE_ECB)
        ct = cipher.encrypt(pad(flag_part, 16)).hex()
        return f"encrypted = {ct}"

    def get_params(self):
        return f"p = {self.p}\ng = {self.g}\nA = {self.A}\nB = {self.B}"


def menu():
    print("\nChoose as you please\n")
    print("1. Get parameters")
    print("2. Reset parameters!! This can take some time")
    print("3. Get Flag")

    option = input("\n> ")
    return option


def main():
    dh = DH()

    while True:
        choice = int(menu())

        # get current parameters
        if choice == 1:
            print(dh.get_params())

        # new parameters
        elif choice == 2:
            dh.gen_params()

        # encrypting the flag
        elif choice == 3:
            print(dh.encrypt(FLAG))
        else:
            print('See you later.')
            exit(1)


if __name__ == "__main__":
    main()
