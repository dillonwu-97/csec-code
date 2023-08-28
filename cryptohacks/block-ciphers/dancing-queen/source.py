#!/usr/bin/env python3

from os import urandom

# https://loup-vaillant.fr/tutorials/chacha20-design

FLAG = b'crypto{?????????????????????????????}'


def bytes_to_words(b):
    return [int.from_bytes(b[i:i+4], 'little') for i in range(0, len(b), 4)]

def rotate(x, n):
    return ((x << n) & 0xffffffff) | ((x >> (32 - n)) & 0xffffffff)

def word(x):
    return x % (2 ** 32)

def words_to_bytes(w):
    return b''.join([i.to_bytes(4, 'little') for i in w])

def xor(a, b):
    return b''.join([bytes([x ^ y]) for x, y in zip(a, b)])


class ChaCha20:
    def __init__(self):
        self._state = []

    def _inner_block(self, state):
        self._quarter_round(state, 0, 4, 8, 12)
        self._quarter_round(state, 1, 5, 9, 13)
        self._quarter_round(state, 2, 6, 10, 14)
        self._quarter_round(state, 3, 7, 11, 15)
        self._quarter_round(state, 0, 5, 10, 15)
        self._quarter_round(state, 1, 6, 11, 12)
        self._quarter_round(state, 2, 7, 8, 13)
        self._quarter_round(state, 3, 4, 9, 14)

    # how to reverse the quarter rounds?
    def _quarter_round(self, x, a, b, c, d):
        x[a] = word(x[a] + x[b]); x[d] ^= x[a]; x[d] = rotate(x[d], 16)
        x[c] = word(x[c] + x[d]); x[b] ^= x[c]; x[b] = rotate(x[b], 12)
        x[a] = word(x[a] + x[b]); x[d] ^= x[a]; x[d] = rotate(x[d], 8)
        x[c] = word(x[c] + x[d]); x[b] ^= x[c]; x[b] = rotate(x[b], 7)
    

    # 1634760805, 857760878, 2036477234, 1797285236
    # the state values are the same as well
    # One potential issue is that the state is not updated?
    # Chacha20 adds the original state and modified state to produce the keystream but this is not done here?
    # No I think the state is updated at each iteration
    # However, the attacker knows half the block
    # Can something be done with this information?
    # Maybe we can reverse the block if we know at least half the block
    def _setup_state(self, key, iv):
        self._state = [0x61707865, 0x3320646e, 0x79622d32, 0x6b206574] # this is the constant "expand 32-byte k"
        self._state.extend(bytes_to_words(key))
        self._state.append(self._counter)
        self._state.extend(bytes_to_words(iv))

    def decrypt(self, c, key, iv):
        return self.encrypt(c, key, iv)

    # Notes: probably shouldn't start at counter = 1
    def encrypt(self, m, key, iv):
        c = b''
        self._counter = 1
        
        for i in range(0, len(m), 64):
            self._setup_state(key, iv)
            # print(f"state is: {self._state}")
            # input()

            # What is this _inner_block() doing? 
            # this is doing the complete rounds to create the next state?
            for j in range(10):
                self._inner_block(self._state)

            # I see the goal of the problem is to recover the state of the blocks that was used to encrypt the flag 
            # We can recover it by reversing the scrambling tricks that chacha20 uses since we know half the block
            # this is adding unscrambled block to scrambled block?
            c += xor(m[i:i+64], words_to_bytes(self._state)) # # We can use the disclosed plaintext to subtract this part I think

            self._counter += 1
        
        return c
    

# Idea is to use the disclosed message to recover the internal state of the blocks, and then use the internal state of the blocks to recover the flag
if __name__ == '__main__':
    msg = b'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula.' # length = 80
    # key = urandom(32)
    # iv1 = urandom(12)
    # iv2 = urandom(12)

    key = b'a' * 32
    iv1 = b'b' * 12
    iv2 = b'c' * 12

    c = ChaCha20()
    msg_enc = c.encrypt(msg, key, iv1)
    flag_enc = c.encrypt(FLAG, key, iv2)

    print(f"iv1 = '{iv1.hex()}'")
    print(f"iv2 = '{iv2.hex()}'")
    print(f"msg_enc = '{msg_enc.hex()}'") # runs twice 
    print(f"flag_enc = '{flag_enc.hex()}'")
