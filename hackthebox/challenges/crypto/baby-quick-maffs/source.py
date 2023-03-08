#!/usr/bin/env python3
from secret import flag, p, q
from Crypto.Util.number import bytes_to_long
from random import randint


def partition_message(m, N):
    m1 = randint(1, N)
    parts = []
    remainder = 0
    # m = message
    while sum(parts) < m:
        if sum(parts) + m1 < m:
            parts.append(m1)
        else:
            # if sum(parts) + m1 >= m implies that sum(parts) < m, but m1 pushes it over
            # do remainder = m - sum(parts)
            # m1 + remainder
            remainder = m - sum(parts)
            parts.append(m1 + remainder)
    
    # i have the remainder
    # parts is [m1, m1, m1 + remainder]
    # this implies
    # m1 + m1 + remainder = m, the original message
    return (parts, remainder)


def encode(message, N):

    # Assuming that this is the flag
    m = bytes_to_long(message)

    # call partition message on the flag
    parts, remainder = partition_message(m, N)

    # c ^ 2 % N for each c 
    # sqrt(N + ciphers) = parts
    # remainder + parts[0] + parts[1] = message
    # remainder = 
    ciphers = [pow(c, 2, N) for c in parts]
    return (ciphers, remainder)


N = p * q
ciphers, remainder = encode(flag, N)

with open("output.txt", "w") as f:
    out = f'{N}\n{remainder}\n{ciphers}'
    f.write(out)
