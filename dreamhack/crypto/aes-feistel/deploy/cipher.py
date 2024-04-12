from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def xor(a: bytes, b: bytes) -> bytes:
    return bytes([x^y for x,y in zip(a,b)])

class Faestel:
    def __init__(self, key: bytes):
        print("key: ", key.hex())
        self.round = 3
        self.round_keys = self._key_expansion(key)

    def _key_expansion(self, key: bytes) -> list[bytes]:
        assert len(key) == 6
        round_keys = []
        for i in range(self.round):
            round_keys.append(key[i*2:i*2+2]+pad(bytes([i]),14))
        """ print("round_keys: ", round_keys) """
        return round_keys

    def _round_function(self, round_key: bytes, block: bytes):
        f = AES.new(round_key, mode=AES.MODE_ECB).encrypt
        block_l = block[:16]
        block_r = block[16:]
        new_block_l = block_r
        new_block_r = xor(f(block_r), block_l)
        return new_block_l + new_block_r

    def _encrypt(self, block: bytes) -> bytes:
        tmp = block
        """ print("round function before: ", tmp.hex()) """
        for rk in self.round_keys:
            tmp = self._round_function(rk, tmp)
            """ print("round function: ", tmp.hex()) """
        tmp = tmp[16:] + tmp[:16] # another swap here? 
        """ print("round function after: ", tmp.hex()) """
        return tmp

    def _decrypt(self, block: bytes) -> bytes:
        tmp = block
        for rk in self.round_keys[::-1]:
            tmp = self._round_function(rk, tmp)
        tmp = tmp[16:] + tmp[:16]
        return tmp

    def encrypt(self, plaintext: bytes) -> bytes: 
        padded = pad(plaintext, 32)
        ciphertext = b''
        for i in range(0, len(padded), 32):
            ciphertext += self._encrypt(padded[i:i+32]) # so i can brute force each of them basically and work backwards
        return ciphertext

    def decrypt(self, ciphertext: bytes) -> bytes:
        padded = b''
        for i in range(0, len(ciphertext), 32):
            padded += self._decrypt(ciphertext[i:i+32])
        plaintext = unpad(padded, 32)
        return plaintext

if __name__ == '__main__':
    import os
    for i in range(0x1000):
        key = os.urandom(8)
        faestel = Faestel(key)
        pt = os.urandom(32)
        ct = faestel.encrypt(pt)
        de = faestel.decrypt(ct)
        assert pt == faestel.decrypt(ct)
