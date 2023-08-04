import os
from pwn import *
from typing import List
import numpy as np

class PRNG:
    def __init__(self, seed):

        # huh???
        self.p = 0x2ea250216d705
        self.a = self.p
        self.b = int.from_bytes(os.urandom(16), 'big')
        # self.b = 123123123123
        self.rn = seed

    # next value is just the same each time I think, so b is the key??
    def next(self):
        # self.rn is just b?
        self.rn = ((self.a * self.rn) + self.b) % self.p
        return self.rn


def deriveKey(key):
    derived_key = []

    for i, char in enumerate(key):
        previous_letters = key[:i]
        new_number = 1
        # for each of the previous characters
        for j, previous_char in enumerate(previous_letters):
            if previous_char > char:
                derived_key[j] += 1
            else:
                new_number += 1
        derived_key.append(new_number)
    return derived_key

def decrypt(c: str, k: List[int]):
    width: int = 7
    blocks = [c[i:i+width][::-1] for i in range(0,len(c),width)]
    # Mapping the blocks back to their original positions
    # mapping = [None for i in range(len(blocks))]
    mapping = []
    for i in range(len(blocks)):
        mapping.append(blocks[k[i]-1])
    mapping = np.array([list(i) for i in mapping]).transpose().flatten()
    return mapping
    


def solve():
    ciphertexts = [
        'ETYDEDTYAATOSTTUFTEETHIVHMVOSFNANDHEGIIIOCESTHTCHDHNRNYALSRPDAIRDCEEIFREEEEOETLRTRNLEEUNBEOIPYLTNOVEOAOTN',
        'EECNEMOTCYSSSEORIRCETFDUCEDAATAPATWTTSKTTRROCEANHHHAIHOGPTTGROIEETURAFYUIPUEEONOISECNJISAFALRIUAVSAAVPDES',
        'GTNOERUTOIAOTIGRESHHBTSEHLORSRSSNTWINTEAUEENTAEEENOICCAFOSHDORLUFHRIALNGOYPNCEIGTAYAPETHCEOUATEFISTFBPSVK',
        'SNUTCAGPEEPWLHITEDFNDMPNWSHFORSLEOAIPTAPEOOOAOTGOSESNADRITRAEREOSSNPECUHSNHENSAATETTPSIUIUOOHPNSKTNIRYHFT',
        'WFAFDDSGIMMYTADNHRENINONSRSUMNITAHIANSUOEMAAEDAIFLOTFINEAYNEGYSNKROEOGFTCTNLYIIOODLOIRERVTAROTRROUNUTFAUP'
    ]
    k = deriveKey('148823505998502')

    ret = ''
    for c in ciphertexts:
        ret += ''.join(decrypt(c, k))
    print(ret)

def sandbox():

    test = PRNG(int.from_bytes(os.urandom(16), 'big'))
    print(test.next()) # this should just be b
    for i in range(10):
        print(test.next())

    dK = deriveKey('148823505998502')
    print(dK)
    print(len(dK))

    solve()
    

def main(): 
    sandbox()

if __name__ == '__main__':
    main()
    # flag: HTB{THISRNGISNOTSAFEFORGENETINGOUTPUTS}

# 148823505998502 