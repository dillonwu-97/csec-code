from pwn import *
from Crypto.Util.number import long_to_bytes, bytes_to_long

def xor(a, b):
        return b''.join([bytes([_a ^ _b]) for _a, _b in zip(a, b)])

def main():
    ct = 'b25bc89662197c6462188e5960eea4fbef11424b8ebdcd6b45c8f4240d64f5d1981aab0e299ff75ce9fba3d5d78926543e5e8c262b81090aef60518ee241ab131db902d2582a36618f3b9a85a35f52352d5499861b4a878fac1380f520fe13deb1ca50c64f30e98fa6fdc070d02e148f'
    r = 3
    phrases = ['5fe633e7071e690fbe58a9dace6f3606', '501ccdc4600bc2dcf350c6b77fcf2681']
    
    blocks = [ct[i:i+32] for i in range(0, len(ct), 32)]
    br0 = xor(unhex(blocks[r+1]), unhex(phrases[0]))
    br1 = xor(unhex(blocks[r+2]), unhex(phrases[1]))
    print(br0 + br1)
    # Flag: HTB{AES_CFB_15_4_n1c3_m0d3}

if __name__ == '__main__':
    main()