from Crypto.Util.number import bytes_to_long, getStrongPrime
from random import randint

FLAG = b'HTB{????????????????????????????????????????????}'


def key_gen(bits):
    p, q = getStrongPrime(bits), getStrongPrime(bits)
    N = p * q
    return N, (p, q)


def encrypt(m, N, f):
    e1, e2 = randint(2, N - 2), randint(2, N - 2) # two random very large e values
    c1 = (pow(f, e1, N) + m) % N # (p ^ e1 % N) + m % N
    c2 = (pow(f, e2, N) + m) % N # (p ^ e2 % N) + m % N

    return (e1, c1), (e2, c2)

# Thoughts:
# (A mod N - B mod N) mod N = (A - B) mod N <-- this gets rid of m 
# (p^e1 - p^e2) % N
# N and (p^e1 - p^e2) are both divisible by p


def main():
    N, priv = key_gen(1024) # gives N, (p,q)

    m = bytes_to_long(FLAG)

    (e1, c1), (e2, c2) = encrypt(m, N, priv[0]) # encrypt only using p

    with open('out.txt', 'w') as f:
        f.write(f'N = {N}\n(e1, c1) = ({e1}, {c1})\n(e2, c2) = ({e2}, {c2})\n')


if __name__ == "__main__":
    main()
