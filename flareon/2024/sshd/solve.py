from pwn import *


def main():
    path = './rfs/usr/lib/x86_64-linux-gnu/liblzma.so.5.4.1'
    f = open(path, 'rb')
    b = f.read()
    start = 0x00023960
    sz = 0xf96
    sc = b[start:start+sz]
    print(sc.hex())

    temp = open('./temp', 'wb')
    temp.write(sc)
    temp.close()

    f.close()
    


if __name__ == '__main__':
    main()
