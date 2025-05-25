from Crypto.Util.number import *
FLAG = b"CCTF{bbbccccddddaaaabbbbccccddd}" # 32 bytes

# very slow nextPrime function
# trying to find a very close prime
def nextPrime(n):
    while True:
        n += (n % 2) + 1
        if isPrime(n):
            return n

def nb(n, b):
    if n == 0:
        return [0]
    digits = []
    while n:
        digits.append(int(n % b))
        n //= b
    return digits[::-1]

def sandbox():

    # binary representation of the flag
    f = [int(x) for x in bin(int(FLAG.hex(), 16))[2:]]
    # temp = []
    # for x in bin(int(FLAG.hex(),16))[2:]:
    #     temp.append(x)
    # print(len(f))
    # print(f)

    # ensure that f starts with 0
    f.insert(0, 0) # insert at position 0 
    
    # current value is equal to the current value plus the next value, so there is a range (0,2)
    for i in range(len(f)-1): f[i] += f[i+1]
    print(f) 

    a = nextPrime(len(f)) # get a prime of the length of the flag, call it x
    b = nextPrime(a) # get the next prime after that? x += (x % 2) + 1
    print(a, b) # 257, 263
    input()

    # gives me a grid for both g and h
    # for some first prime, and then for some next prime
    # create duplicates
    g, h = [[_ for i in range(x) for _ in f] for x in [a, b]]
    print(g)
    # for i,v in enumerate(g):
    #     print("row: ", i)
    #     print("value: ", v)

    # for i,v in enumerate(f):
    #     print("row: ", i)
    #     print("value: ", v)

    c = nextPrime(len(f) >> 2) # get another prime? # 67
    # the next prime divided by 2??
    # divide by 2
    print(c) 
    print("***Next***" * 50)
    input()
    # for _ in [g, h]:
    for _ in [g]:
        for __ in range(c): _.insert(0, 0) # for each array in g / h, insert 0 to the beginning?
        print(g)

        for i in range(len(_) -  c): _[i] += _[i+c] # for each in the length of the arr minus the new prime, do _[i] + _[i+c]
        input()
        print(g)

    # IDEA: probably some subtraction of h from g to recover the plaintext
    prev_g = g
    g, h = [int(''.join([str(_) for _ in __]), 5) for __ in [g, h]] # convert the pental value to decimal
    print(g)
    print(len(prev_g)) # 65859
    # assert(nb(g, 5) == prev_g)

    # for _ in [g, h]:
    #     if _ == g:
    #         fname = 'g'
    #     else:
    #         fname = 'h'
    #     of = open(f'{fname}.enc', 'wb')
    #     of.write(long_to_bytes(_))
    #     of.close()



# Reversing the process / deducing how big the flag / prime is
def solve():
    g = open("./g.enc", 'rb').read()
    h = open("./h.enc", 'rb').read()

    # Recover
    five_g = nb(bytes_to_long(g), 5) # 65859
    five_h = nb(bytes_to_long(h), 5) # 67395
    print(five_g)
    print(len(five_g))
    print(len(five_h))
    five = [five_g, five_h]

    # Recovered two primes
    # length of g is: 257
    # length of h is: 263
    # length of c is: 67
    clen = 67

    # work backwards by subtracting
    for x in five:
        for i in range(len(x) -  clen-1, -1, -1):
            x[i] -= x[i+clen]

    assert(five[0][1] == 0)
    assert(five[1][1] == 0)

    five[0] = five[0][clen:]
    five[1] = five[1][clen:]


    for x in five:
        for i in range(len(x) - 2, -1, -1):
            x[i] -= x[i+1]


    print("*" * 100)
    print(five[0])
    five[0] = five[0][1:]
    five[1] = five[1][1:]

    ans = ''.join([str(i) for i in five[0]])
    ans = int(ans, 2)
    print(long_to_bytes(ans))
    

    
    


def main():
    # sandbox()
    solve()

if __name__ == '__main__':
    main()
