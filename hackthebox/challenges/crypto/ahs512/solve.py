from pwn import *
from base64 import *
from requests import *
from Crypto.Util.number import bytes_to_long, long_to_bytes


# why isn't it consistent and why is the output so weird?

def solve():
    pt = "pumpkin_spice_latte!"
    for j,c in enumerate(pt):

        b = ord(c)
        rb = ((b >> 4) | (b << 3)) & 0xff
        print("*" * 10)
        print("Character: ", c)
        for i in range(256):
            if ((i >> 4) | (i << 3)) & 0xff == rb and i != b:
                print("Found i: ", i, chr(i))
                temp = list([ord(i) for i in pt])
                temp[j] = i
                return temp
                # return "".join(temp)

def main():
    print("[*] Starting solve")
    ret = solve()
    
    s = "".join([hex(i)[2:].zfill(2) for i in ret])
    print(s)
    # print("".join([chr9i.encode().hex() for i in ret]))

if __name__ == '__main__':
    main()


# Flag: HTB{5h4512_8u7_w17h_4_7w157_83f023_c4n_93n32473_c0111510n5}
