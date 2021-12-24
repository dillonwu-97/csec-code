import string
from pwn import *
import json
# 2^128 collision protection!
BLOCK_SIZE = 32

# Nothing up my sleeve numbers (ref: Dual_EC_DRBG P-256 coordinates)
W = [0x6b17d1f2, 0xe12c4247, 0xf8bce6e5, 0x63a440f2, 0x77037d81, 0x2deb33a0, 0xf4a13945, 0xd898c296]
X = [0x4fe342e2, 0xfe1a7f9b, 0x8ee7eb4a, 0x7c0f9e16, 0x2bce3357, 0x6b315ece, 0xcbb64068, 0x37bf51f5]
Y = [0xc97445f4, 0x5cdef9f0, 0xd3e05e1e, 0x585fc297, 0x235b82b5, 0xbe8ff3ef, 0xca67c598, 0x52018192]
Z = [0xb28ef557, 0xba31dfcb, 0xdd21ac46, 0xe2a91e3c, 0x304f44cb, 0x87058ada, 0x2cb81515, 0x1e610046]

# Lets work with bytes instead!
W_bytes = b''.join([x.to_bytes(4,'big') for x in W])
X_bytes = b''.join([x.to_bytes(4,'big') for x in X])
Y_bytes = b''.join([x.to_bytes(4,'big') for x in Y])
Z_bytes = b''.join([x.to_bytes(4,'big') for x in Z])

def pad(data):
    padding_len = (BLOCK_SIZE - len(data)) % BLOCK_SIZE
    print(padding_len)
    ret = data + bytes([padding_len]*padding_len)
    print(ret)
    return ret

def blocks(data):
    return [data[i:(i+BLOCK_SIZE)] for i in range(0,len(data),BLOCK_SIZE)]

def xor(a,b):
    return bytes([x^y for x,y in zip(a,b)])

def rotate_left(data, x):
    x = x % BLOCK_SIZE
    return data[x:] + data[:x]

def rotate_right(data, x):
    x = x % BLOCK_SIZE
    return  data[-x:] + data[:-x]

def scramble_block(block):
    for _ in range(40):
        block = xor(W_bytes, block)
        block = rotate_left(block, 6)
        block = xor(X_bytes, block)
        block = rotate_right(block, 17)
    return block

def cryptohash(msg):
    initial_state = xor(Y_bytes, Z_bytes)
    msg_padded = pad(msg)
    msg_blocks = blocks(msg_padded)
    for i,b in enumerate(msg_blocks):
        print(i)
        mix_in = scramble_block(b)
        for _ in range(i):
            mix_in = rotate_right(mix_in, i+11)
            mix_in = xor(mix_in, X_bytes)
            mix_in = rotate_left(mix_in, i+6)
        initial_state = xor(initial_state,mix_in)
    return initial_state.hex()

def main():
    # Bug is with the padding
    # print(cryptohash(b'hello'))
    # for i in string.ascii_lowercase:
    #     print(cryptohash(i.encode()))
    s1 = b'a'
    s2 = b'a\x1f\x1f\x1f\x1f\x1f\x1f\x1f\x1f\x1f\x1f\x1f\x1f\x1f\x1f\x1f\x1f\x1f\x1f\x1f\x1f\x1f\x1f\x1f\x1f\x1f\x1f\x1f\x1f\x1f\x1f\x1f'
    print(s2.hex())
    print(s1.hex())
    print(cryptohash(s1))
    print(cryptohash(s2))
    assert (cryptohash(s1) == cryptohash(s2))
    s1 = s1.hex()
    s2 = s2.hex()
    
    # s1 = 'a'.encode()
    # s1 = '0a'
    # s2 = '0b'
    # # s2 = 'b'.encode()
    data = {"m1":s1, "m2":s2}
    # # data = {"m1":s1.decode(), "m2":s2.decode()}
    payload = json.dumps(data)
    HOST = 'socket.cryptohack.org'
    PORT = 13405
    r = remote(HOST, PORT)
    r.recvuntil("JSON: ")
    ret = r.sendline(payload)
    ret = r.recvline()
    print(ret)

    # Flag: crypto{Always_add_padding_even_if_its_a_whole_block!!!}


if __name__ == '__main__':
    main()
