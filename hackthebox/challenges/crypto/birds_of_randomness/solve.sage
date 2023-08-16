from ecdsa import ellipticcurve as ecc
from pwn import *
from Crypto.Util.number import isPrime

LOCAL = False
if LOCAL:
    r = remote('localhost', 1337)
else:
    r = remote('157.245.43.189', 30848)

class TR:
    def __init__(self, Gx, Gy, x, y, z):
        self.p = 17101937747109687265202713197737423
        self.Gx = Gx
        self.Gy = Gy
        self.ec_order = 17101937747109687496599931614463506
        self.E = ecc.CurveFp(self.p, 2, 3)
        self.G = ecc.Point(self.E, self.Gx, self.Gy, self.ec_order)
        self.x = x
        self.y = y
        self.z = z
        #self.seed = int(self.x) + 1, int(self.y) + 1, int(self.z) + 1
        self.seed = x, y, z

    def rotate(self):
        x, y, z = self.seed # iteratively get the next seed using a linear congruential generator
        x = (171 * x) % 30269
        y = (172 * y) % 30307
        z = (170 * z) % 30323
        self.seed = x, y, z

    def goToNextStation(self):
        while True:
            self.rotate()
            x, y, z = self.seed

            if(isPrime(x) and isPrime(y) and isPrime(z)):
                d = x * y * z
                new_point = d * self.G 
                return int(new_point.x()), int(new_point.y())

def solve_ecdlp(start, target):
    '''
    Steps to solving this problem:
    The elliptic group is a composite number so factor that number first
    Use pollig-hellman algorithm to find the generators for the subgroups
    Use crt to recover the value d
    Factor d into the three separate prime values
    Create combinations for the three prime values

    :param start: starting point on the elliptic curve
    :param target: target point on the elliptic curve
    '''
    ec_order = 17101937747109687496599931614463506
    primes = factor(ec_order)
    dlogs = []
    for i,v in enumerate(primes): 
        p = v[0] # the prime
        t = ec_order // p 
        print("t: ", t)
        d = discrete_log(t * target, t * start, operation="+")
        dlogs.append(d)
    ret = crt(dlogs, [p[0] for p in primes])
    print(ret)
    return factor(ret)


def solve():
    start = r.recvline().decode().strip('\n').split(":")[1]
    Tx = int(start.split(",")[0].replace("(", "").replace(" ", "")) # target point for dlp
    Ty = int(start.split(",")[1].replace(")", "").replace(" ", "")) # target point for dlp

    p = 17101937747109687265202713197737423
    a = 2
    b = 3
    Gx = 3543321030468950376213178213609418
    Gy = 14807290861072031659976937040569354

    EC = EllipticCurve(GF(p), [a,b])
    start = EC(Gx, Gy)
    target = EC(Tx, Ty)
    factors = solve_ecdlp(start, target)
    x,y,z = factors[0][0], factors[1][0], factors[2][0]

    for i,v in enumerate(Permutations([x,y,z]).list()):
        l = r.recvline()
        print(v[0], v[1], v[2])
        print(l)
        tr = TR(Gx, Gy, v[0], v[1], v[2])
        # tr = TR(Tx, Ty, v[0], v[1], v[2]) # Does not work with this
        # Does this work with Tx, Ty instead?
        Dx, Dy = tr.goToNextStation()
        print(Dx, Dy)
        l = r.recvuntil(": ")
        print(l)
        r.sendline(str(Dx))
        r.recvuntil(": ")
        r.sendline(str(Dy))
        print("Sent! ")
    print("Finished")



def main():
    solve()
    # Flag: HTB{PRNGs,math,ECC_and_crypto_>_love._Love_is_pain}

if __name__ == '__main__':
    main()
