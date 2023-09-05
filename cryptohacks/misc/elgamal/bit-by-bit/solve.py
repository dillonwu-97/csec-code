# legendre symbols since there is a 4 that is used to multiply the ciphertext with so it serves as a recovery tool
from ast import literal_eval
from Crypto.Util.number import long_to_bytes

def legendre(v,q):
    return pow(v, (q-1)//2, q)


def solve():
    q = 117477667918738952579183719876352811442282667176975299658506388983916794266542270944999203435163206062215810775822922421123910464455461286519153688505926472313006014806485076205663018026742480181999336912300022514436004673587192018846621666145334296696433207116469994110066128730623149834083870252895489152123
    f = open("./output.txt", "r").read().split("\n")
    ret = ''
    for i,v in enumerate(f):
        if i % 2 == 0:
            continue
        t = v.split(", c2=0x")[1]
        c2 = int(t[:-1], 16)
        # no extra bit was added
        temp = legendre(c2, q)
        if temp == 1:
            ret = '1' + ret
        # extra bit added and it is not a quadratic residue
        elif temp == q-1:
            ret = '0' + ret
        else:
            print("oops")
    print(ret)
    print(long_to_bytes(int(ret, 2)))


def main():
    solve()
    # flag: crypto{s0m3_th1ng5_4r3_pr3served_4ft3r_encrypti0n}

if __name__ == '__main__':
    main()
