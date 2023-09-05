from pwn import *
from hashlib import sha256
from Crypto.Util.number import long_to_bytes

PRIME = 77793805322526801978326005188088213205424384389488111175220421173086192558047

# Try making some deterministic shares
def make_deterministic_shares(minimum, shares, secret, prime):
    if minimum > shares:
        raise ValueError("Pool secret would be irrecoverable.")

    coefs = [secret]
    for i in range(1, shares + 1):
        coef = hashlib.sha256(coefs[i-1]).digest()
        coefs.append(coef)
    
    coefs = [int.from_bytes(p, 'big') for p in coefs]
    poly = coefs[:minimum]

    points = []
    for i in range(1, shares + 1):
        point = _eval_at(poly, coefs[i], prime)
        points.append((coefs[i], point))

    return points

# This is done in reverse order because we want to start with the coefficient corresponding to the polynomial with the highest degree
def _eval_at(poly, x, prime):
    accum = 0
    for coeff in reversed(poly):
        accum *= x
        accum += coeff
        accum %= prime
    return accum

def get_next_n_coeff(start: bytes, n: int):
    coefs = [start]
    for i in range(1,n+1):
        new_coef = sha256(coefs[i-1]).digest()
        coefs.append(new_coef)
    coefs = [int.from_bytes(c, 'big') for c in coefs]
    return coefs

def get_next_n_points(poly: list[int]):
    points = []
    for i,v in enumerate(poly):
        point = _eval_at(poly, v, PRIME) 
        points.append((v, point))
    return points

def sandbox():
    FLAG = b'crypto{???????????????????????}'
    shares = make_deterministic_shares(minimum=3, shares=7, secret=FLAG, prime=PRIME)
    given = shares[0]
    print(shares)
    print(f"[*] The share we are given is: {given}")

    n = 3
    print(f"Trying to reconstruct the next {n} shares")
    start = bytes.fromhex(hex(given[0])[2:])
    recon_coefs = get_next_n_coeff(start, n)
    for i,v in enumerate(recon_coefs):
        assert v == shares[i][0]
    print("Successfully reconstructed next {n} shares")

    print(f"Trying to reconstruct the next {n} points")
    # i dont think i can reconstruct the points like this actually
    # this is because i dont have the secret so i dont have the very first polynomial
    # in sss, i would need the points to reconstruct what i need but i only have one point
    recon_points = get_next_n_points(recon_coefs)
    assert len(recon_points) == n+1
    for i,v in enumerate(recon_points):
        print(v, shares[i])
        assert(v[1] == shares[i][1])
        assert(v[0] == shares[i][0])
    

def solve():
    shared = (105622578433921694608307153620094961853014843078655463551374559727541051964080, 25953768581962402292961757951905849014581503184926092726593265745485300657424)
    point_1 = shared[1]
    coef_1 = bytes.fromhex(hex(shared[0])[2:])
    
    
    deduce = int.from_bytes(sha256(coef_1).digest(), 'big')
    # point_1 = secret + given_0 * given_0 + deduce_0 * given_0 * given_0
    secret = (shared[1] - shared[0] * shared[0] - shared[0] * shared[0] * deduce) % PRIME
    print(long_to_bytes(secret))


def main():
    solve()
    # flag: crypto{fr46m3n73d_b4ckup_vuln?}

if __name__ == '__main__':
    main()
