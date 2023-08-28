from pwn import *
from ast import literal_eval
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib

r = remote('socket.cryptohack.org', 13380)

def is_pkcs7_padded(message):
    padding = message[-message[-1]:]
    return all(padding[i] == len(padding) for i in range(0, len(padding)))


def decrypt_flag(shared_secret: int, iv: str, ciphertext: str):
    # Derive AES key from shared secret
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode('ascii'))
    key = sha1.digest()[:16]
    # Decrypt flag
    ciphertext = bytes.fromhex(ciphertext)
    iv = bytes.fromhex(iv)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)

    if is_pkcs7_padded(plaintext):
        return unpad(plaintext, 16).decode('ascii')
    else:
        return plaintext.decode('ascii')
def solve():
    d = r.recvline().decode().strip("\n").split("Alice: ")[1]
    d = literal_eval(d)
    print(d)
    p = int(d['p'][2:],16)
    g = int(d['g'][2:],16)
    A = int(d['A'][2:],16)

    print(p)
    print(g)
    print(A)

    g_inv = pow(g, -1, p)
    print(g_inv)

    d = r.recvline().decode().strip("\n").split("Bob: ")[1]
    d = literal_eval(d)
    B = int(d['B'][2:], 16)

    a = (g_inv * A) % p
    print(a)

    print("[*] Recovered shared key")
    sk = (B * a) % p
    print(f"Shared key: {sk}")

    d = r.recvline().decode().strip("\n").split("Alice: ")[1]
    d = literal_eval(d)
    iv = d['iv']
    enc = d['encrypted']

    print(decrypt_flag(sk, iv, enc))

def main():
    solve()
    # Flag: crypto{cycl1c_6r0up_und3r_4dd1710n?}

if __name__ == '__main__':
    main()
