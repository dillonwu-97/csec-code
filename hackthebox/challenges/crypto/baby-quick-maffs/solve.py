import math
import gmpy2
from Crypto.Util.number import long_to_bytes


def main():
    gmpy2.get_context().precision = 100000
    n = 6083782486455360611313889289556658208725888944237734041722591252756006664878102248734673207367745303402874595854966731263105387801996693270011840173939423

    r = 1081087287982224274239399953615475281184099226198643053396569433856757255106426461817760194704250226883807897800355728788149068771546876055268915238961343
    
    ciphers = [5408283916250636369066846815501131861319520431106165986129813106223074286810632222888292034380612581416458756909119954039579666773680866532576166358987272, 5408283916250636369066846815501131861319520431106165986129813106223074286810632222888292034380612581416458756909119954039579666773680866532576166358987272, 5598555010250184271123226314796180406367795504188162611960100902143581636125416986623404842897202277277978566659455918773104687212096435095590205751904580]

    # cipher[-1] = m1 + remainder
    # remainder = m - sum(parts) = m - (cipher[0] + cipher[1]) = m - cipher[0] - cipher[1]
    # m1 is some random value

    # m1 ^ 2 + 2 * r * m1 + r ^2 % N = z 
    m12 = ciphers[0] % n
    r_sq = pow(r, 2, n)
    r_db = (r * 2) % n
    z = ciphers[2] % n

    diff = (z - m12 - r_sq) % n
    print(diff, r_db)
    print(diff % r_db)
    # 2*r*ml = z, solve for ml
    print(math.gcd(r_db, n))
    inv = gmpy2.invert(r_db, n)
    assert ((r_db * inv) % n == 1)
    m1 = (diff * inv) % n
    print(m1)
    assert (pow(m1, 2, n) == ciphers[0])
    m = m1 + m1 + r
    print(long_to_bytes(m))


    # print(m12, r2)
    # Flag: HTB{d0nt_ev4_r3l4ted_m3ss4ge_att4cks_th3y_ar3_@_d3a1_b7eak3r!!!}

if __name__ == '__main__':
    main()