#!/usr/bin/env python3

import hashlib
from Crypto.Util.number import long_to_bytes

FLAG = b"crypto{???????????????????????}"
PRIME = 77793805322526801978326005188088213205424384389488111175220421173086192558047

# this is interesting, why is reversed(poly) used?
def _eval_at(poly, x, prime):
    accum = 0
    for coeff in reversed(poly):
        accum *= x
        accum += coeff
        accum %= prime
    return accum


# the flag is the secret value used
# 
def make_deterministic_shares(minimum, shares, secret, prime):
    if minimum > shares:
        raise ValueError("Pool secret would be irrecoverable.")

    coefs = [secret]
    
    # grab the digest of the previous coefficient, so need coefs[0] to recover the rest of the coefficients
    for i in range(1, shares + 1):
        coef = hashlib.sha256(coefs[i-1]).digest()
        coefs.append(coef)
    
    # make them integers
    coefs = [int.from_bytes(p, 'big') for p in coefs]
    # grab the minimum number of required coefficients
    poly = coefs[:minimum]

    # for each share that we want to create, get a point
    # the secret gets removed here since we only use the next few coefficients
    points = []
    for i in range(1, shares + 1):
        point = _eval_at(poly, coefs[i], prime)
        points.append((coefs[i], point))

    return points


shares = make_deterministic_shares(minimum=3, shares=7, secret=FLAG, prime=PRIME)

# which coefficient got generated? for this coefficient, we can technically generate the next forward coefficients, but maybe not the backward coefficients? 
# I can just generate the new coefficients for this problem, recover the polynomial that intersects all three points and from there, get the first polynomial on the line?? 
# so graphically, get the next three polynomials. After getting the next three polynomials, go back a distance of three to get the first polynomial to get the secret
# print(FLAG)
for share in shares:
    print(share)
    print(long_to_bytes(share[0]))
