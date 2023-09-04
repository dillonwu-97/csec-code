from Crypto.Util.number import long_to_bytes, inverse

def gauss_red(v1, v2):
    while(1):
        if v2.norm() < v1.norm():
            v2, v1 = v1, v2
        m = (v1*v2) // (v1*v1)
        if m == 0:
            return v1, v2
        v2 -= m* v1

def decrypt(q, h, f, g, e):
    a = (f*e) % q
    m = (a*inverse(f, g)) % g
    return m

def main():
    q = 7638232120454925879231554234011842347641017888219021175304217358715878636183252433454896490677496516149889316745664606749499241420160898019203925115292257 
    h = 2163268902194560093843693572170199707501787797497998463462129592239973581462651622978282637513865274199374452805292639586264791317439029535926401109074800
    enc_flag = 5605696495253720664142881956908624307570671858477482119657436163663663844731169035682344974286379049123733356009125671924280312532755241162267269123486523

    # the matrix built is: 
    # h 
    # [1, 0]
    # [h, q]
    # The linear equation we are solving is:
    # f * h = g mod q
    # f*h - qn = g
    # [f] [h, -q]
    # [n] [1, 0]
    # f * h - n * q = g
    # f * 1 + 0 = f
    # Solving this system of equations gives us g and f
    # So the vectors we are use are column-wise so vectors are (h, 1) and (-q, 0)
    v1 = vector([h, 1])
    v2 = vector([-q,0])
    v3, v4 = gauss_red(v1, v2)
    print(v3)
    print(v4)
    g = v3[0]
    f = v3[1]
    assert(h * f ) %q == g
    print(long_to_bytes(decrypt(q, h, f, g, enc_flag)))


if __name__ == '__main__':
    # Flag: crypto{Gauss_lattice_attack!}
    main()
