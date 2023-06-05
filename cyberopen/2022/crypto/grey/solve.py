from pwn import *

# grey = grey encoding
# minimize bit changes

def solve():
    p = remote('0.cloud.chals.io', 11444)
    p.recvuntil("Username:")
    p.sendline("mgrey")
    p.recvuntil("Password:")
    p.sendline("1515")

    flag = 0
    for i in range(16):
        for j in range(0, 1<<10):
            gray = j^ (j >> 1)
            if gray >= 1000:
                continue
            if flag == 0:
                if i >= 13:
                    a = p.recvline()
                    recv_val = p.recvline()
                    print(a, recv_val)
                else:
                    recv_val = p.recvuntil("):")
                if b'Correct Code' in recv_val:
                    print("Found:" ,gray)
                    flag = 1
                    break
            else: 
                flag = 0
            print("received: ", recv_val)
                        #print(str(gray).zfill(3))
            p.sendline(str(gray).zfill(3))

    p.recvline()
    p.recvline()
    p.recvline()
    p.recvline()


def main():

    # Testing out grey bit generator
    '''
    n = 10
    for i in range(0, 1 << n):
        if i == 1000:
            break
        gray = i^ (i >> 1)
        print ("{0:0{1}b}".format(gray,n))
    '''

    solve()


if __name__ == '__main__':
    main()
    # uscg{Gr4y_c0d3S}
