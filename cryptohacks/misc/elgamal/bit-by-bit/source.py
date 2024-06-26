from Crypto.Random import random
from Crypto.Util.number import getPrime, bytes_to_long

FLAG = b'crypto{??????????????????????????????????????????}'


# Elgamal uses diffie helman somewhere
# elgamal does key generation, encryption, decryption
def get_padding():
    seed = 256
    e = random.randint(2, q)

    # 256 ^ e % q
    padding = pow(seed, e, q)
    return padding


def public_key():

    # random public key raised to generator mod q
    # this is the h value := pow(g, x, q)
    x = random.randint(2, q)
    return pow(g, x, q)


# encrypt a message m using a reversible mapping function
# g^x^y % q

def encrypt(m, h):
    y = random.randint(2, q)
    s = pow(h, y, q)
    c1 = pow(g, y, q)
    c2 = (s * m) % q
    return (c1, c2)


m = bytes_to_long(FLAG)

# this prime is a sophie germain prime unfortunately
q = 117477667918738952579183719876352811442282667176975299658506388983916794266542270944999203435163206062215810775822922421123910464455461286519153688505926472313006014806485076205663018026742480181999336912300022514436004673587192018846621666145334296696433207116469994110066128730623149834083870252895489152123

g = 104831378861792918406603185872102963672377675787070244288476520132867186367073243128721932355048896327567834691503031058630891431160772435946803430038048387919820523845278192892527138537973452950296897433212693740878617106403233353998322359462259883977147097970627584785653515124418036488904398507208057206926

# what is the point of the padding?
# I need to recover the last bit
while m:
    padding = get_padding()

    # precedence is m%2, then that + 1, so 1 + 1 -> 2, 0 + 1 -> 1
    me = padding << 1 + m % 2 # so last bit is saved. what is the point of the padding then?
    h = public_key()
    (c1, c2) = encrypt(me, h)
    print(f'(public_key={hex(h)})')
    print(f'(c1={hex(c1)}, c2={hex(c2)})')
    m //= 2 # shift the message to the right
