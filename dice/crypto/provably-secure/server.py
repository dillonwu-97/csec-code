#!/usr/local/bin/python

# Normally you have unlimited encryption and decryption query requests in the IND-CCA2 game.
# For performance reasons, my definition of unlimited is 8 lol

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from secrets import randbits
from os import urandom
from Crypto.Util.strxor import strxor

def encrypt(pk0, pk1, msg):
    r = urandom(16) # r
    r_prime = strxor(r, msg) # r ^ message
    ct0 = pk0.encrypt(r, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                         algorithm=hashes.SHA256(), label=None))
    ct1 = pk1.encrypt(r_prime, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), 
                         algorithm=hashes.SHA256(), label=None))

    # First part is r encrypted, second part is r ^ msg encrypted
    return ct0.hex() + ct1.hex()


def decrypt(key0, key1, ct):
    ct0 = ct[:256]
    ct1 = ct[256:]
    r0 = key0.decrypt(ct0, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                           algorithm=hashes.SHA256(), label=None))
    r1 = key1.decrypt(ct1, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                           algorithm=hashes.SHA256(), label=None))
    # r0 = r
    # r1 = r ^ msg
    # r0 ^ r1 = r ^ r ^ msg = msg
    # decrypt gives us back the message
    # but what if in the decryption step we send nothing <- cannot do this
    # We can encrypt multiple plaintexts and then decrypt using different keys though?
    return strxor(r0, r1)

# Goal is to guess the correct bit 128 times
if __name__ == '__main__':
    print("""Actions:
0) Solve
1) Query Encryption
2) Query Decryption
""")
    # going through 128 experiments
    for experiment in range(1, 129):
        print("Experiment {}/128".format(experiment))

        # get some private key
        key0 = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        key1 = rsa.generate_private_key(public_exponent=65537, key_size=2048)

        # get the public key from this private key
        pk0 = key0.public_key()
        pk1 = key1.public_key()

        # Is there any point in this information? Is it at all useful to know the modulo? I don't think so
        print("pk0 =", pk0.public_numbers().n)
        print("pk1 =", pk1.public_numbers().n)
        m_bit = randbits(1)

        seen_ct = set() # convert any iterable to sequence of iterable elements with distinct elements, i.e. find unique ciphertexts?
        
        # encrypt count, decrypt count
        en_count = 0
        de_count = 0
        
        while True:
            choice = int(input("Action: "))
            if choice == 0:
                guess = int(input("m_bit guess: "))
                if (guess == m_bit):
                    print("Correct!")
                    break
                else:
                    print("Wrong!")
                    exit(0)
            elif choice == 1:
                en_count += 1
                if (en_count > 8):
                    print("You've run out of encryptions!")
                    exit(0)

                # What are m0 and m1?
                m0 = bytes.fromhex(input("m0 (16 byte hexstring): ").strip())
                m1 = bytes.fromhex(input("m1 (16 byte hexstring): ").strip())
                if len(m0) != 16 or len(m1) != 16:
                    print("Must be 16 bytes!")
                    exit(0)
                
                # Try to understand how the encryption is leaking information
                # Need to verify if the ciphertext is m0 or m1
                msg = m0 if m_bit == 0 else m1
                ct = encrypt(pk0, pk1, msg)
                seen_ct.add(ct)
                print(ct)
                # Ciphertext is composed of two partitions; can I recover r? Recover r might not help
                # We are given the ciphertext which is a combination of pk0 and pk1
            
            elif choice == 2:
                de_count += 1
                if (de_count > 8):
                    print("You've run out of decryptions!")
                    exit(0)
                in_ct = bytes.fromhex(input("ct (512 byte hexstring): ").strip())
                if len(in_ct) != 512:
                    print("Must be 512 bytes!")
                    exit(0)
                if in_ct in seen_ct:
                    print("Cannot query decryption on seen ciphertext!")
                    exit(0)
                print(decrypt(key0, key1, in_ct).hex())

    with open('flag.txt', 'r') as f:
        print("Flag: " + f.read().strip())