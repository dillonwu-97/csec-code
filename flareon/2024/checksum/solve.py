import base64
from Crypto.Cipher import ChaCha20_Poly1305
import pgpy


b64_str = 'cQoFRQErX1YAVw1zVQdFUSxfAQNRBXUNAxBSe15QCVRVJ1pQEwd/WFBUAlElCFBFUnlaB1ULByRdBEFdfVtWVA=='
bites = base64.b64decode(b64_str)
const = 0x5d1745d1745d1746
const = -2096220917466994502


# 101110100010111010001011101000101110100010111010001011101000110
xor_str = 'FlareOn2024'
def get_nonce_and_key():
    print(bites, len(bites))

    """ mov     rsi, rax """
    """ mov     rax, 0x5d1745d1745d1746 """
    """ mov     rdi, rdx """
    """ imul    rbx """
    """ sar     rdx, 0x2 """
    """ lea     r8, [rdx+rdx*4] """
    """ lea     rdx, [rdx+r8*2] """
    """ mov     rax, rbx """
    """ sub     rax, rdx """
    """ movzx   edx, byte [rbx+rdi] """
    """ cmp     rax, 0xb """
    """ jb      0x4a77ea """

    # rbx = counter 
    counter = 0 
    rdi = 'A' * 64 # input 
    to_check = ''

    for i in range(0x100000):
        b = const * i
        print(b, len(bin(b)[3:][:-64]))
        b = bin(b)[3:] # get rid of the negative and 0b characters
        b = b[:-64] # grab the upper bits 
        if len(b) == 0:
            b = '0'
        hi = int(b, 2) >> 2
        counter = i - (hi * 11)
        print("hi: ", hi, "counter: ", counter)
        assert counter >= 0
        print(i, counter)
        if counter >= 11: 
            break 
        cur = ord(rdi[i]) ^ ord(xor_str[counter])
        to_check += hex(cur)[2:].zfill(2)
        
    print(to_check,len(to_check))
    
        
def reverse_the_enc():

    ret = b''
    for i in range(len(bites)):
        temp = bites[i] ^ ord(xor_str[i % len(xor_str)])
        assert temp < 256
        ret += temp.to_bytes(1, byteorder='little')
    """ print("val: ", ret.hex()) """
    """ print(base64.b64encode(ret[:32])) """
    """ print(ret[:32].hex()) """
    return ret

def check(to_check):
    ret = b''
    for i in range(len(bites)):
        temp = to_check[i] ^ ord(xor_str[i % 11])
        ret += temp.to_bytes(1, byteorder='little')
    ret += bites[len(xor_str):]
    assert ret == bites
    assert base64.b64encode(ret).decode() == b64_str


def get_enc_file():
    f = open('./checksum.exe', 'rb').read()
    start = 0
    for i in range(len(f)):
        if (f[i:i+8].hex()[2:] == 'bdcbfa0ecd079b'):
            start = i
            break
            input()
    enc_file = f[start: start+0x2c52c]
    assert enc_file.hex()[2:8] == 'bdcbfa'
    return enc_file

    
# okay, so the key could be wrong 
def decrypt(val, enc):
    cipher = ChaCha20_Poly1305.new(key=val[:0x20], nonce=val[:0x18])
    dec = cipher.decrypt(enc)
    print(dec[:8].hex())
    f = open('./temp', 'wb')
    f.write(dec)
    f.close()

def another_dec(key, val):
    dec = b''
    assert len(key) == 64
    for i in range(len(val)):
        """ temp = val[i] ^ ord(xor_str[i % 11]) """
        temp = val[i] ^ key[i % len(key)]
        dec += temp.to_bytes(1, byteorder='little')

    f = open('./temp', 'wb')
    f.write(dec)
    f.close()

def handle_pgp():
    s = open('./pgpkey', 'rb')
    sec_key, _ = pgpy.PGPKey.from_blob(s)
    print(sec_key)
 
def sandbox():
    """ get_nonce_and_key() """
    key = reverse_the_enc()
    print(key)
    enc = get_enc_file()
    """ decrypt(key, enc) """
    another_dec(key, enc)
    """ handle_pgp() """

    
def main():

    # sandbox testing
    """ sandbox() """

    print("base64 decoded: ", base64.b64decode(b64_str)) # length = 64
    print("decoded base64 flag with xor key: ", reverse_the_enc().decode()) # this is a hash
    hash_bytes = bytes.fromhex(reverse_the_enc().decode())
    assert len(hash_bytes) == 0x20
    print("hash bytes: ", hash_bytes, len(hash_bytes))
    enc = get_enc_file()
    decrypt(hash_bytes, enc)





if __name__ == '__main__':
    main()
    # flag: Th3_M4tH_Do_b3_mAth1ng@flare-on.com
