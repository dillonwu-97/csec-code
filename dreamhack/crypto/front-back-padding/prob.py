#!/usr/bin/env python3

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import os

from flag import FLAG

prefix = b'DreamHack_prefix'
suffix = b'happy_Amo_suffix'

def FB_pad(msg):
    r = -len(msg)%16 + 16
    n1 = r // 2
    n2 = r - n1
    return prefix[:n1] + msg + suffix[-n2:]

def FB_unpad(msg):
    if len(msg) % 16 != 0:
        return False, "message length is invalid"
    n1 = 0
    n2 = 0
    while n1 < 16 and msg[:n1 + 1] == prefix[:n1 + 1]:
        n1 += 1
    while n2 < 16 and msg[-n2 - 1:] == suffix[-n2 - 1:]:
        n2 += 1
    if n1 + n2 < 16:
        return False, "wrong padding"
    return True, msg[n1:-n2]


def main():
    key = os.urandom(16)
    iv = os.urandom(16)
    print("iv: ", iv.hex())

    print('I wonder. Why is padding always located at the back of a message?')
    print('Forget about that stupid padding method. Front-Back padding, this one is much more better.')
    print('1. Encypt message')
    print('2. Decrypt message')
    print('3. Get the encrypted flag')

    while True:
        action = int(input(' > '))
        if action == 1:
            cipher = AES.new(key, AES.MODE_CBC, iv)
            msg = input('input your message(hex) > ')
            msg = bytes.fromhex(msg)
            msg = FB_pad(msg)
            ciphertext = cipher.encrypt(msg)
            print(f'here is your encrypted message: {ciphertext.hex()}')
        
        elif action == 2:
            cipher = AES.new(key, AES.MODE_CBC, iv)
            msg = input('input your message(hex) > ')
            msg = bytes.fromhex(msg)
            plaintext = cipher.decrypt(msg)
            print(plaintext)
            sc, output = FB_unpad(plaintext)
            if not sc:
                print('failed due to error:', output)
            else:
                print(f'here is your decrypted message: {output.hex()}')
        
        elif action == 3:
            print('Amo accidentally padded my flag in a stupid way :<')

            cipher = AES.new(key, AES.MODE_CBC, iv)
            ciphertext = cipher.encrypt(pad(FLAG, 16))
            print(f'take my stupid flag: {ciphertext.hex()}')

if __name__ == '__main__':
    main()
