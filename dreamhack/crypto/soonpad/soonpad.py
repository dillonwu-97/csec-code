#!/usr/bin/python3

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import random
""" from flag import flag """

""" flag_1 = flag[:100] # very big flag? """
""" flag_2 = flag[100:] """
""" flag_1 = "A" * 47 + "ZZ" + "Z" * 47 + "BCDE" """
flag_1 = 'HHFT@NDSCILLHAAPRLLF@RPRCNJRJCQGKSIOMOGJQCBLBNAGJNPHSENMPIDHOQFECABMQDMRJPOOI@MHKESMGKGHTOMKFKMMTPJE'
flag_2 = 'HHFT@NDSCILLHAAPRLLF@RPRCNJRJCQGKSIOMOGJQCBLBNAGJNPHSENMPIDHOQFECABMQDMRJPOOI@MHKESMGKGHTOMKFKMMTPJE'

pad_string = "soon_haari_loser"

def soonpad(pt):
    # ex: -5 % 16 = 11
    pad_len = -len(pt) % 16
    if pad_len == 0:
        pad_len = 16
    pt_padded = pt + pad_string[:pad_len]
    assert len(pt_padded) % 16 == 0

    return pt_padded

def encrypt(pt):
    cipher = AES.new(random.randbytes(16), AES.MODE_ECB)
    ct = cipher.encrypt(pad(pt, 16)) # ok there is another bit of extra padding that is added for some reason which i dont feel like is necessary
    return ct

print("soonpad will replace pkcs7 within few years")

while 1:
    msg = input("message: ")

    if msg == flag_1:
        break
    # i think this half is kind of solved?
    print("passed")
    pt = soonpad(msg + flag_1)
    print("pt is: ", pt)
    print(bytes.hex(encrypt(pt.encode())))

print("\nSo???.. Second one??")

while 1:
    msg = input("message: ")

    if msg == flag_2:
        break

    print('msg: ', msg, len(msg), msg.encode(), len(msg.encode()))
    print(soonpad(msg))
    """ print(pad((soonpad(msg) + soonpad(flag_2)).encode(), 16)) """
    print(soonpad(flag_2))

    pt = soonpad(msg) + soonpad(flag_2) # flag2 is not controllable
    print(bytes.hex(encrypt(pt.encode())))

print("Not bad!! https://tenor.com/view/nice-click-nice-man-guy-gif-21933845")
