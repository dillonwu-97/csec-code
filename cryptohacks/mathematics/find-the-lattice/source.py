from Crypto.Util.number import getPrime, inverse, bytes_to_long
import random
import math

FLAG = b'crypto{?????????????????????}'


def gen_key():
    q = getPrime(512)
    upper_bound = int(math.sqrt(q // 2)) # 512 bits / 2 -> 511 bits, sqrt(511 bits) -> 255-256 bits
    lower_bound = int(math.sqrt(q // 4)) # 512 bits / 4 -> 510 bits, sqrt(510 bits) -> 255 bits
    f = random.randint(2, upper_bound) # so getting a random number up to 256 bits
    while True:
        g = random.randint(lower_bound, upper_bound) # get another random number between 255 -> 256 bits
        # make sure that they are coprime
        if math.gcd(f, g) == 1: 
            break
    # get the inverse of f and some prime q, and then multiply it by some value g. (q,h) are public keys. (f,g) are private keys 
    # which makes sense the modulos are public
    h = (inverse(f, q)*g) % q
    return (q, h), (f, g)


def encrypt(q, h, m):
    assert m < int(math.sqrt(q // 2))
    r = random.randint(2, int(math.sqrt(q // 2))) # get a random integer up to 256 bits

    # generate the value e
    # isnt r a random value?
    e = (r*h + m) % q # r * h (h is public) + m mod q 
    return e


def decrypt(q, h, f, g, e):
    # f is a private key, g is a private key
    # e is a public key, so multiply that with a private key f and take the mod
    # e is (r*h + m) % q
    # a = ((r*h + m) % q) * f
    # m = a * inverse(f, g) meaning f * inverse = 1 mod g so that basically cancels out the *f from a leaving us with e?
    # how the decrytion works:
    # h = (f_h * g) % q
    # e = r * h + m % q
    # e = [r * (f_h * g % q) + m] % q
    # a = (f * e) % q
    # a = f * ([r * (f_h * g % q) + m] % q) % q
    # a = (f % q) * ([r * (f_h * g % q) + m] % q) % q
    # a = ((f * r * f_h * g) % q + (f * m) % q) % q
    # a = (r * g % q) + f * m % q
    # m = (a * f_g) % g
    # m = ((r * g * f_g) % q + (f * f_g * m) % q) % g 
    # first term disappears since anything * g % g gives 0 and f * f_g gives 1

    a = (f*e) % q
    m = (a*inverse(f, g)) % g
    return m


public, private = gen_key()
q, h = public
f, g = private

m = bytes_to_long(FLAG)
e = encrypt(q, h, m)

print(f'Public key: {(q,h)}')
print(f'Encrypted Flag: {e}')
