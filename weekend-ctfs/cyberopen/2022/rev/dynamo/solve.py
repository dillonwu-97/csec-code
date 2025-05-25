# Notes:
# need to find the base of main?? the address is stripped or something like that
# Anti disassembly
from pwn import *

def main():


    # arr
    arr = [0x9f, 0x3f, 0x98, 0xa4, 7, 0x35, 0x70, 0x77, 0x49, 0x1b, 0x27, 0x46, 0x5e, 0x20, 0x4e, 0xbd, 0x7f, 0x92, 199, 0xfc, 0x8b, 0x86, 0xc, 0xc6, 0x15, 0xc9, 0x45]
    
    # ret
    ret = [0x2e, 0xd2, 0xb7, 0xa8, 0x23, 0xc9, 0xc, 0x9f, 0x68, 0xcf, 0x7e, 0x67, 0x25, 0x69, 0x6e, 0xe2, 0x42, 0x43, 100, 0xaa, 0xed, 0x3a, 0xec, 0xf4, 0xaa, 0x99, 0xb9]
    arr += [0] * (32 - len(arr))
    ret += [0] * (40 - len(ret))

    param = [0] * 40

    # just a simple swap
    for i in range(0, 0xd):
        if i+1 < 0x1b:
            temp = ret[i]
            ret[i] = ret[i+1]
            ret[i+1] = temp

            # ret[i], ret[i+1] = ret[i+1], ret[i]

    for i in range(0, 0x1a):
        ret[i+1] = ret[i] ^ ret[i+1]
        if (ret[i+1] > 256): input()

    for i in range(0, 0x1b):
        arr[i] = arr[i] + 0x17
        if arr[i] > 256: 
            arr[i] = arr[i] - 256
            print(arr[i])
            # arr[i] = 256 - arr[i]
            input()

    for i in range(0, 0x1b):
        param[i] = (ret[i] ^ arr[i])
        if param[i] > 256:
            print(param[i])
            input()
    param = param[:0x1b]
    print(len(param))
    
    print(param)
    print(''.join([chr(i) for i in param]))

    # uscg{d3bU9g3Rs_4r3_c00L_8da39b72}
if __name__ == '__main__':
    main()
