from re import I
from sage.all import *
import string, base64, math

ALPHABET = string.printable[:62] + '\\='
F = list(GF(64))
def sandbox():
    enc = '805c9GMYuD5RefTmabUNfS9N9YrkwbAbdZE0df91uCEytcoy9FDSbZ8Ay8jj'
    
    F = list(GF(64))
    print('hello world')
    print(ALPHABET)
    print(F)
    key = 1
    for i in range(128):
        print("Value: ", key**5 + key**3 + key**2 + 1 * F[35])

def maptofarm(v):
    return F[ALPHABET.index(v)]

def decrypt(ct, key):
    pkey = key ** 5 + key ** 3 + key ** 2 + 1
    pt = ''
    for i,v in enumerate(ct):
        pt += ALPHABET[F.index(F[ALPHABET.index(v)] / pkey)]

    return base64.b64decode(pt)

# the numbers exist in the galois extension field
def solve():
    ciphertext = '805c9GMYuD5RefTmabUNfS9N9YrkwbAbdZE0df91uCEytcoy9FDSbZ8Ay8jj'
    # 1-to-1 mapping

    '''
    Idea:
    For each character in the ciphertext:
        get the index -> i = alphabet.index(c)
        this is the product of the key and some plaintext -> multiplier = F[i]
        try for each key
            the first few characters are cctf, which map to specific values in the field
    '''

    print(ALPHABET)
    plaintext = base64.b64encode(b'CCTF{').decode()
    mult = [F[ALPHABET.index(c)] for c in plaintext] 
    prod = [F[ALPHABET.index(c)] for c in ciphertext][:5]
    print(mult)
    print(prod)

    # for i in range(64):
    #     key = F[i]
    #     pkey = key ** 5 + key ** 3 + key ** 2 + 1
    #     if pkey * mult[0] == prod[0] and pkey * mult[1] == prod[1] and pkey * mult[2] == prod[2]:
    #         print(key, i)

    # index = 30
    key = F[30]
    print(decrypt(ciphertext, key))
    



def main():
    solve()

if __name__ == '__main__':
    main()