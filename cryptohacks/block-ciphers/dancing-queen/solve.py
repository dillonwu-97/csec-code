from pwn import *
from random import getrandbits
from source import ChaCha20

def bytes_to_words(b):
    return [int.from_bytes(b[i:i+4], 'little') for i in range(0, len(b), 4)]

def words_to_bytes(w):
    return b''.join([i.to_bytes(4, 'little') for i in w])

def rotate(x, n):
    return ((x << n) & 0xffffffff) | ((x >> (32 - n)) & 0xffffffff)

def reverse_rotate(x, n):
    return ((x >> n) & 0xffffffff) | ((x << (32 - n)) & 0xffffffff)

def xor(a, b):
    return b''.join([bytes([x ^ y]) for x, y in zip(a, b)])

def word(x):
    return x % (2 ** 32)

def reverse_mod(a, b):
    '''
    a is the residue, b is the known value, return value is the original
    '''
    if (a > b):
        return a - b
    else:
        return (a + 2**32) - b

def quarter_round(x, a, b, c, d):
    x[a] = word(x[a] + x[b]); x[d] ^= x[a]; x[d] = rotate(x[d], 16)
    x[c] = word(x[c] + x[d]); x[b] ^= x[c]; x[b] = rotate(x[b], 12)
    x[a] = word(x[a] + x[b]); x[d] ^= x[a]; x[d] = rotate(x[d], 8)
    x[c] = word(x[c] + x[d]); x[b] ^= x[c]; x[b] = rotate(x[b], 7)

# Going in reverse from bottom up
def reverse_quarter(x, a, b, c, d):
    x[b] = reverse_rotate(x[b], 7); x[b] ^= x[c]; x[c] = reverse_mod(x[c], x[d])
    x[d] = reverse_rotate(x[d], 8); x[d] ^= x[a]; x[a] = reverse_mod(x[a], x[b])
    x[b] = reverse_rotate(x[b], 12); x[b] ^= x[c]; x[c] = reverse_mod(x[c], x[d])
    x[d] = reverse_rotate(x[d], 16); x[d] ^= x[a]; x[a] = reverse_mod(x[a], x[b])

def inner_block(state):
    quarter_round(state, 0, 4, 8, 12)
    quarter_round(state, 1, 5, 9, 13)
    quarter_round(state, 2, 6, 10, 14)
    quarter_round(state, 3, 7, 11, 15)
    quarter_round(state, 0, 5, 10, 15)
    quarter_round(state, 1, 6, 11, 12)
    quarter_round(state, 2, 7, 8, 13)
    quarter_round(state, 3, 4, 9, 14)

def reverse_inner(state):
    reverse_quarter(state, 3, 4, 9, 14)
    reverse_quarter(state, 2, 7, 8, 13)
    reverse_quarter(state, 1, 6, 11, 12)
    reverse_quarter(state, 0, 5, 10, 15)
    reverse_quarter(state, 3, 7, 11, 15)
    reverse_quarter(state, 2, 6, 10, 14)
    reverse_quarter(state, 1, 5, 9, 13)
    reverse_quarter(state, 0, 4, 8, 12)


def setup_state(key, iv, counter):
    state = []
    state = [0x61707865, 0x3320646e, 0x79622d32, 0x6b206574]
    state.extend(bytes_to_words(key))
    state.append(counter)
    state.extend(bytes_to_words(iv))
    return state


def encrypt(m, key, iv):
    c = b''
    counter = 1
    for i in range(0, len(m), 64):
        state = setup_state(key, iv, counter)
        for j in range(10):
            inner_block(state)
        c += xor(m[i:i+64], words_to_bytes(state))

        counter += 1
    return c

# Trying to recover the key now
def recover_key(c, m, iv):
    counter = 1
    key = None
    for i in range(0, len(c), 64):
        state = xor(c[i:i+64], m[i:i+64])
        state = bytes_to_words(state)
        for j in range(10):
            reverse_inner(state)
        print(state)
        key = words_to_bytes(state[4:12])
        break
    return key


def sandbox():
    print("[*] Testing reverse_rotate function")
    a = [getrandbits(32) for i in range(100)]
    for i,v in enumerate(a):
        for j in range(10):
            assert (reverse_rotate(rotate(v, j), j) == v)
    print("[*] Reverse_rotate function ok ")

    print("[*] Testing reverse_mod function")
    b = [getrandbits(32) for i in range(100)]
    for i,v in enumerate(a):
        c = word(a[i] + b[i])
        d = reverse_mod(c, b[i])
        assert(a[i] == d)
    print("[*] Reverse_mod function ok")

    print("[*] Testing quarter round reverse")
    state = [getrandbits(32) for i in range(16)]
    e = state.copy()
    quarter_round(state, 3, 4, 9, 14)
    d = state.copy()
    reverse_quarter(state, 3, 4, 9, 14)
    flag = 0
    for i in range(len(state)):
        assert(state[i] == e[i])
        if (state[i] != d[i]):
            flag = 1
    assert (flag == 1)
    print("[*] Quarter round reverse ok")

    print("[*] Testing inner block reverse")
    f = state.copy()
    inner_block(state)
    g = state.copy()
    for i in range(len(state)):
        assert(state[i] != f[i])
    reverse_inner(state)
    for i in range(len(state)):
        assert(state[i] != g[i])
        assert(state[i] == f[i])
    print("[*] Inner block reverse ok")

    print("[*] Testing encrypion")
    m = b'h' * 64
    key = b'b' * 32
    iv = b'c' * 12
    enc = encrypt(m, key, iv)
    dec = encrypt(enc, key, iv)
    assert (dec == m)
    print("[*] Normal enc dec ok")

    print("[*] Trying to recover the key")
    k = recover_key(enc, m, iv)
    print(k)
    assert (k == key)
    print("[*] Successfully recovered the key")

def solve():
    iv1 = bytes.fromhex('e42758d6d218013ea63e3c49')
    iv2 = bytes.fromhex('a99f9a7d097daabd2aa2a235')
    msg = b'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula.'[:64]
    msg_enc = bytes.fromhex('f3afbada8237af6e94c7d2065ee0e221a1748b8c7b11105a8cc8a1c74253611c94fe7ea6fa8a9133505772ef619f04b05d2e2b0732cc483df72ccebb09a92c211ef5a52628094f09a30fc692cb25647f')[:64]
    flag_enc = bytes.fromhex('b6327e9a2253034096344ad5694a2040b114753e24ea9c1af17c10263281fb0fe622b32732')
    key = recover_key(msg_enc, msg, iv1)
    print(key)
    assert(len(key) == 32)

    cipher = ChaCha20()
    flag_dec = cipher.encrypt(flag_enc, key, iv2)
    print(flag_dec)
    # Flag: crypto{M1x1n6_r0und5_4r3_1nv3r71bl3!}



def main():
    sandbox()
    solve()

if __name__ == '__main__':
    main()

