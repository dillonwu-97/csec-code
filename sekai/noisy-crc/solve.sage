from pwn import *
from ast import literal_eval
from collections import Counter
from Crypto.Cipher import AES
from hashlib import sha256
from Crypto.Util.number import long_to_bytes

#r = remote('chals.sekai.team', 3005)
r = remote('localhost', 9999)
F = GF(2)
R.<x> = PolynomialRing(F)

def get_send_poly(irreducible):
    '''
    Get the polynomials I need to send
    '''
    to_send = []
    for i in range(100):
        temp = R.random_element(12) * irreducible
        if temp not in to_send:
            to_send.append(temp)
    return to_send

def get_send_int(poly_to_send):
    to_send = []
    for i,v in enumerate(poly_to_send):
        to_send.append( ZZ(list(v), 2) )
    return to_send

def get_residues(int_to_send: list):
    ret = []
    for i,v in enumerate(int_to_send):
        r.recvuntil(": ")
        r.sendline(str(v))
        temp = r.recvline().decode().strip('\n')
        l = literal_eval(temp)
        ret.append(l)
    return ret
        
def build_dict(noisy_residues: list, irreducible):
    d = Counter()
    for i,v in enumerate(noisy_residues):
        for j,w in enumerate(v):
            temp = R( ZZ(w).bits() )
            temp %= irreducible
            d[temp] += 1
    return d

def recover_true_res(noisy_residues, irreducible, top):
    '''
    Get the true residues
    '''
    ret = []
    indices = []
    for i,v in enumerate(noisy_residues):
        temp_arr = []
        for j,w in enumerate(v):
            temp = R ( ZZ(w).bits() )
            if temp % irreducible == top:
                temp_arr.append(temp)
        if len(temp_arr) == 1:
            ret.append(temp_arr[0])
            indices.append(i)
    return ret, indices
                
def solve():
    flag_enc = r.recvline().decode().strip('\n').split(": ")[1]
    irreducible = R.irreducible_element(4)
    print("[*] Grabbing polynomials and ints")
    poly_to_send = get_send_poly(irreducible)
    int_to_send = get_send_int(poly_to_send)
    print("[*] Making sure they are equal")
    for i,v in enumerate(int_to_send):
        assert R( v.bits() ) == poly_to_send[i]
    print("[*] Grabbing the residues")
    noisy_residues = get_residues(int_to_send)
    freq_dict = build_dict(noisy_residues, irreducible)
    top_freq = max( freq_dict, key=freq_dict.get)
    print(f"Found top freq: {top_freq} with count: {freq_dict[top_freq]}")
    true_residues, indices = recover_true_res(noisy_residues, irreducible, top_freq)
    print(true_residues[0]) # the remainders
    print("[*] Getting the indices of the polynomials")
    poly_to_use = []
    for i in indices:
        poly_to_use.append(poly_to_send[i])
    assert(len(poly_to_use) == len(true_residues))
    key_poly = crt(true_residues, poly_to_use) 
    key = int( ZZ( list(key_poly), 2) ) // (1<<16)
    cipher = AES.new(sha256(long_to_bytes(key)).digest()[:16], AES.MODE_CTR, nonce=b"12345678")
    flag = cipher.decrypt(bytes.fromhex(flag_enc))
    print(flag)
    # flag: SEKAI{CrCrCRcRCRcrcrcRCrCrC}

    

def sandbox2():
    flag_enc = r.recvline().decode().strip('\n').split(": ")[1]
    F = GF(2)
    R.<x> = PolynomialRing(F)

    # Idea being that polynomial of degree 4 * polynomial of degree 12 will give me a polynomial of degree 16 when converted into an integer
    irreducible = R.irreducible_element(4)
    int_rr = ZZ ( list (irreducible), 2 )

    p_to_send = []
    for i in range(100):
        temp = R.random_element(12) * irreducible
        if temp not in p_to_send:
            p_to_send.append(temp)

    print(p_to_send)

    # convert to integers to send 
    ints_to_send = []
    for i,v in enumerate(p_to_send):
        ints_to_send.append( ZZ( list(v.change_ring(ZZ)), 2 ) ) # converting the polynomials into integers
    print(ints_to_send)

    residues = []
    responses = []
    for i,v in enumerate(ints_to_send):
        r.recvuntil(": ")
        r.sendline(str(v))
        temp = r.recvline().decode().strip('\n')
        l = literal_eval(temp)
        for j,w in enumerate(l):
            poly_w = R(ZZ(w).bits())
            temp = poly_w % irreducible
            residues.append(temp)
        responses.append(residues)

    # We can see the number that produced the mos
    d = Counter(residues)
    top = ( max(d, key=d.get))
    crt_values = []
    crt_mods = []

    assert(len(responses) == len(ints_to_send))
    print(d)

    # Problem: there exists some duplicates
    for i,v in enumerate(responses):
        flag = 0
        flag_index = 0
        for j,w in enumerate(v):
            #print(w, irreducible, top)
            if ( w % irreducible == top):
                flag +=1
                flag_index = j
            if flag == 1:
                crt_mods.append( R(ZZ(ints_to_send[i]).bits()) )
                crt_values.append( v[flag_index] )
                print("flag is 1")
            else:
                print("flag is 0")

    print(crt_values)
    print(crt_mods)
    print(len(crt_values), max(d, key=d.get))
    print(d)
    assert( len(crt_values) == len(crt_mods))
    
    key = CRT_list(crt_values, crt_mods)
    print("key: ", key)

def sandbox():
    '''
    flag_enc = r.recvline().decode().strip('\n').split(": ")[1]
    print("flag enc: ", flag_enc)
    r.recvuntil(": ")
    payload = 1 << 16
    r.sendline(str(payload))
    r.interactive()
    '''
    F = GF(2)
    #R.<x> = PolynomialRing(F) # global
    R = PolynomialRing(F, 'x')
    p = R.irreducible_element(3)
    print(p)

    print(R.random_element(0))
    print(R.random_element(1))
    print(R.random_element(12))
    print(p.is_irreducible())

    print("Testing change ring")
    first = list(p.change_ring(ZZ))
    second = list(p)
    print(ZZ(list(second), 2))
    print(ZZ(list(first), 2))

def main():
    #sandbox()
    solve()



if __name__ == '__main__':
    main()
