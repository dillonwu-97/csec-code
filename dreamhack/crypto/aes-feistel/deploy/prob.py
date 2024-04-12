#!/usr/bin/env python3
import os
from cipher import Faestel, xor

def menu() -> int:
    print('1. encrypt')
    print('2. flag')
    print('3. exit')
    i = int(input('> '))
    return i

if __name__ == '__main__':
    with open('flag', 'rb') as f:
        flag = f.read()

    key = os.urandom(6)
    faestel = Faestel(key)

    while True:
        i = menu()
        if i == 1:
            pt = input('plaintext(hex)> ')
            ct = faestel.encrypt(bytes.fromhex(pt))
            print(f'ciphertext(hex)> {ct.hex()}')
        elif i == 2:
            newkey = xor(key, b'faeste')
            newfaestel = Faestel(newkey)
            enc_flag = newfaestel.encrypt(flag)
            print(f'encrypted flag(hex)> {enc_flag.hex()}')
        elif i == 3:
            print('bye~')
            exit()
        else:
            print('invalid option')
