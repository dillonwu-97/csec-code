from pwn import *
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
from deploy.cipher import Faestel, xor

LOCAL =False 
if LOCAL:
    r = remote('localhost', 1119)
else:
    r = remote('host3.dreamhack.games', 24430)

def xor(a: bytes, b: bytes) -> bytes:
    return bytes([x^y for x,y in zip(a,b)])

'''
Steps to solving the problem
1) leak f(b) by setting a to 0
2) make a = f(b) so a ^ f(b) = 0
'''

# building dictionary for the 0 value
def build_enc_f1():
    d = {}
    pt = '00' * 16
    pt = bytes.fromhex(pt)
    assert len(pt) == 16
    for i in range(2**16):
        key = i.to_bytes(2, 'big') + pad(bytes([0]),14)
        f = AES.new(key, mode=AES.MODE_ECB).encrypt
        ct = f(pt)
        assert len(ct.hex()) == 32
        d[ct.hex()] = i
    return d

def receive_enc(pt):
    print(r.recvline())
    r.sendlineafter("> ", "1") 
    r.sendlineafter("> ", pt) # extra padding of \x01
    vals = []
    """ for i in range(5): """
    """     l = r.recvline().decode().split(": ")[1].strip('\n') """
    """     print(l) """
    """ print(r.recvline()) """
    """ print(r.recvline()) """
    """ print(r.recvline()) """
    """ print(r.recvline()) """
    """ print(r.recvline()) """
    ct = r.recvline().decode().split("> ")[1].strip('\n')
    ct = ct[:64]
    assert len(ct) == 64
    """ print("ct: ", ct) """
    return ct

def build_dec_f2(ct):
    d = {}
    ct = bytes.fromhex(ct)
    for i in range(2**16):
        key = i.to_bytes(2, 'big') + pad(bytes([1]),14)
        f = AES.new(key, mode=AES.MODE_ECB).decrypt
        pt = f(ct)
        assert len(pt.hex()) == 32
        d[pt.hex()] = i
    return d

def get_f3(l, r, f1_enc):
    l = bytes.fromhex(l)
    f1_enc = bytes.fromhex(f1_enc)
    for i in range(2**16):
        key = i.to_bytes(2, 'big') + pad(bytes([2]),14)
        f = AES.new(key, mode=AES.MODE_ECB).encrypt 
        candidate = xor ( f(l), f1_enc ).hex()
        if candidate == r:
            return hex(i)[2:]
                                               
    

    
# crack the first layer in 2^32 operations
def main():
    """ r = process('./deploy/prob.py') """
    """ print(r.recvline()) """
    
    # Precalculation 

    pt = "00" * 32
    assert len(pt) == 64
    receive_enc(pt)
    f1_dict = build_enc_f1()
    ct = receive_enc(pt)
    a = pt[:32]
    b = pt[32:]
    e = ct[:32]
    d = ct[32:]

    """ print(d) # f_b ^ f_d """
    f2_dict = build_dec_f2(d)
    f1 = None
    f2 = None
    f1_enc = None
    for i in f2_dict:
        if i in f1_dict:
            print("Found!")
            print("second byte: ", hex(f2_dict[i]))
            print("first byte: ", hex(f1_dict[i]))
            f1_enc = i
            f1 = hex(f1_dict[i])[2:]
            f2 = hex(f2_dict[i])[2:]
            break

    f3 = get_f3(d, e, f1_enc)
    key = bytes.fromhex(f1+f2+f3)
    print("key: ", key.hex())
    # step 1:

    r.sendlineafter("> ", "2")
    flag = r.recvline().decode().split("> ")[1][:-1]
    print("flag enc: ", flag)

    print(key.hex(), b'faeste'.hex())
    newkey = xor(key, b'faeste')
    assert len(newkey) == 6
    newfaestel = Faestel(newkey)
    dec_flag = newfaestel.decrypt(bytes.fromhex(flag))
    print(dec_flag)
    # DH{24ec68b35e5b863c61ba62d86c30d7ce589d779dcd8a}

    

if __name__ == "__main__":
    main()
