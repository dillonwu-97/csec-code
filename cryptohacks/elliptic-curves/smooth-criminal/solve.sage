from pwn import *
from base64 import *
from requests import *
from Crypto.Util.number import bytes_to_long, long_to_bytes
# from tinyec import registry
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib
from collections import namedtuple
from Crypto.Util.number import inverse
from random import randint
import os

Point = namedtuple("Point", "x y")
p = 310717010502520989590157367261876774703
a = 2
b = 3
def check_point(P: tuple):
    if P == O:
        return True
    else:

        # return the following elliptic curve equation?
        return (P.y**2 - (P.x**3 + a*P.x + b)) % p == 0 and 0 <= P.x < p and 0 <= P.y < p


def point_inverse(P: tuple):
    if P == O:
        return P
    return Point(P.x, -P.y % p)


def point_addition(P: tuple, Q: tuple):
    # based of algo. in ICM
    if P == O:
        return Q
    elif Q == O:
        return P
    elif Q == point_inverse(P):
        return O
    else:
        if P == Q:
            lam = (3*P.x**2 + a)*inverse(2*P.y, p)
            lam %= p
        else:
            lam = (Q.y - P.y) * inverse((Q.x - P.x), p)
            lam %= p
    Rx = (lam**2 - P.x - Q.x) % p
    Ry = (lam*(P.x - Rx) - P.y) % p
    R = Point(Rx, Ry)
    assert check_point(R)
    return R

def sandbox2():
    curve = registry.get_curve('secp192r1')
    print('curve:', curve)
    print(f"Generator is: {curve.g}")

    for k in range(0, 10):
        p = k * curve.g
        print(f"{k} * G = ({p.x}, {p.y})")

    print("Cofactor =", curve.field.h)
    print('Cyclic group order =', curve.field.n)
    nG = curve.field.n * curve.g
    print(f"n * G = ({nG.x}, {nG.y})")

def sandbox():
    g_x = 179210853392303317793440285562762725654
    g_y = 105268671499942631758568591033409611165
    G = Point(g_x, g_y)

    d = {}
    i = 0
    while(1):
        public_candidate = double_and_add(G, i)
        print(f"Iteration: {i}")
        print(public_candidate)
        if public_candidate[0] not in d:
            d[public_candidate[0]] = public_candidate[1]

        elif public_candidate[0] == 280810182131414898730378982766101210916:
            print("Found something!")
            input()
        else:
            print("Found something!", public_candidate[0])
            input()
            
        i+=1
    cpoint = (280810182131414898730378982766101210916, 291506490768054478159835604632710368904)
    # equation: y^2 = x^3 + a * x + b (mod p)
    a = 2
    b = 3
    p = 310717010502520989590157367261876774703

    assert (pow(cpoint[1],2,p) == ( pow(cpoint[0],3,p) + 2 * cpoint[0] + b  ) % p )
    # for i in range(100):

    # Goal is to recover the value n?

def solve_ecdlp(start, target, factors, o):
    # Solving the Chinese Remainder theorem problem using the factors
    # Is there something wrong with this implementation?
    # dlogs = []
    # for i, v in enumerate(factors):
    #     p = v[0]
    #     t = o // p
    #     # solving the discrete log problems for smaller values?
    #     d = discrete_log(t * target, t * start, operation="+")
    #     dlogs.append(d)
    # ret = crt(dlogs, [v[0] for v in factors])
    # return ret

    moduli = []
    remainders = []
    factors = [f[0] ^ f[1] for f in factors] # turns out you need to raise it to this power??? 
    # did not know this
    for i in factors:
        P0 = start*ZZ(o/i)
        Q0 = target*ZZ(o/i)
        moduli.append(i)
        remainders.append(discrete_log(Q0,P0, operation = '+'))
    return crt(remainders,moduli)
    

def is_pkcs7_padded(message):
    padding = message[-message[-1]:]
    return all(padding[i] == len(padding) for i in range(0, len(padding)))


def decrypt_flag(shared_secret: int, iv: str, ciphertext: str):
    # Derive AES key from shared secret
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode('ascii'))
    key = sha1.digest()[:16]
    # Decrypt flag
    ciphertext = bytes.fromhex(ciphertext)
    iv = bytes.fromhex(iv)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)

    if is_pkcs7_padded(plaintext):
        return unpad(plaintext, 16).decode('ascii')
    else:
        return plaintext.decode('ascii')

def double_and_add(P: tuple, n: int):
    # based of algo. in ICM
    Q = P
    R = O
    while n > 0:
        if n % 2 == 1:
            R = point_addition(R, Q)
        Q = point_addition(Q, Q)
        n = n // 2
    assert check_point(R)
    return R

def gen_shared_secret(Q: tuple, n: int):
    # Bob's Public key, my secret int
    S = double_and_add(Q, n)
    return S.x

def solve():
    # the goal is to solve the discrete log problem for smooth numbers?
    # it could also be even easier than this 
    F = GF(p)
    E = EllipticCurve(F, [a,b])
    E_ord = E.order()
    factors = factor(E_ord)
    g_x = 179210853392303317793440285562762725654
    g_y = 105268671499942631758568591033409611165
    start = E(g_x, g_y)

    send_x = 280810182131414898730378982766101210916
    send_y = 291506490768054478159835604632710368904

    # Solving the discrete lop problem over elliptic curves
    target = E(send_x, send_y)
    # sk = solve_ecdlp(start, target, factors, E_ord)
    sk = 47836431801801373761601790722388100620
    print(sk)
    print(factor(sk))
    primes = factor(sk)
    print(double_and_add(Point(g_x,g_y), sk))
    for i,v in enumerate(primes):
        print(v)
        temp = Point(g_x, g_y)
        print(double_and_add(temp, int(v[0])))
    # the output of this print statement should be the same as send_x and send_y

    
    b_x = 272640099140026426377756188075937988094
    b_y = 51062462309521034358726608268084433317
    shared_secret = gen_shared_secret(Point(b_x, b_y), sk)
    iv = '07e2628b590095a5e332d397b8a59aa7'
    ciphertext = '8220b7c47b36777a737f5ef9caa2814cf20c1c1ef496ec21a9b4833da24a008d0870d3ac3a6ad80065c138a2ed6136af'

    print(decrypt_flag(shared_secret, iv, ciphertext))



def main():
    print("[*] Starting solve")
    # sandbox()
    solve()
    # Flag: crypto{n07_4ll_curv3s_4r3_s4f3_curv3s}

if __name__ == '__main__':
    main()


