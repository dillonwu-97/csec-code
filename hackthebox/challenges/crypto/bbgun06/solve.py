# https://landonhemsley.com/bleichenbacher-06-rsa-signature-forgery-what-they-assume-you-know/ 

# this is the writeup

from pwn import *
import subprocess
from encryption import RSA
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from Crypto.PublicKey import RSA as PYRSA
from Crypto.Util.number import bytes_to_long, long_to_bytes
from hashlib import sha1
import gmpy2


def pad(message, target_length):
    max_message_length = target_length - 11
    message_length = len(message)

    if message_length > max_message_length:
        raise OverflowError(
            "%i bytes needed for message, but there is only"
            " space for %i" % (message_length, max_message_length))

    padding_length = target_length - message_length - 3
    print("OK")
    return b"".join(
        [b"\x00\x01", padding_length * b"\xff", b"\x00", message])

def sandbox():
    LOCAL = False
    if LOCAL:
        # command = ['python', 'server.py']
        # subprocess.run(command)

        r = remote('localhost', 1337)

    else: 
        r = remote('157.245.43.189', 30549)

    l = r.recvline()
    sig = l.decode().split(': ')[1].strip('\n')
    print(bytes.fromhex(sig))
    l = r.recvline()
    pk = r.recvuntil("-----END PUBLIC KEY-----\n").decode().encode("utf-8")
    temppk = serialization.load_pem_public_key(pk, backend=default_backend())
    n = temppk.public_numbers().n
    e = temppk.public_numbers().e
    print(n, e)

    r = myRSA(n)

    # user is what we need to sign
    user = b'IT Department <it@cloudcompany.com>'
    val = int(gmpy2.root(int(sig, 16),3)) ** 3
    temp = long_to_bytes(val).hex()
    print(len(temp))
    #print(long_to_bytes(val))
    #print(n - bytes_to_long(bytes.fromhex(sig)))

def solve():
    LOCAL = False
    if LOCAL:
        # command = ['python', 'server.py']
        # subprocess.run(command)

        r = remote('localhost', 1338)
        pass

    else: 
        r = remote('157.245.39.76', 31751)

    # header = b'\x00\x01\xff\x00' # Note: in() will not work for this string because \x00 is in the string
    header = b'\x00\x01\xff\x00'
    asn1 = b"\x30\x21\x30\x09\x06\x05\x2b\x0e\x03\x02\x1a\x05\x00\x04\x14"
    sha = sha1(b'IT Department <it@cloudcompany.com>').digest()
    assert(len(asn1) == 15)
    assert(len(sha) == 20)
    print(header, asn1, sha)
    gmpy2.get_context().precision = 10000

    l = r.recvline()
    sig = l.decode().split(': ')[1].strip('\n')
    print(bytes.fromhex(sig))
    l = r.recvline()
    pk = r.recvuntil("-----END PUBLIC KEY-----\n").decode().encode("utf-8")
    temppk = serialization.load_pem_public_key(pk, backend=default_backend())
    n = temppk.public_numbers().n

    payload = header + asn1 + sha
    to_send = payload
    # for i in range(100000):
    #     temp = payload + (b'\xff' * i) # add garbage to the end
    #     # print(payload, temp)
    #     temp = long_to_bytes(int(gmpy2.root(bytes_to_long(temp),3)) ** 3)
    #     # print(payload, temp)
    #     if (payload in temp):
    #         to_send = temp
    #         break

    # Sending payload to get flag
    to_send += (len(long_to_bytes(n)) - len(to_send)) * b'\xff'
    assert (payload in to_send)
    l = r.recvuntil("hex: ")
    print(l)
    print(to_send, len(long_to_bytes(n)))
    # to_send = pad(to_send, len(long_to_bytes(n)))
    to_send = long_to_bytes(int(gmpy2.root(bytes_to_long(to_send), 3))) # this is correct
    print(long_to_bytes(bytes_to_long(to_send) ** 3))
    # assert(payload in long_to_bytes(bytes_to_long(to_send) ** 3))
    to_send = to_send.hex()
    print(to_send)
    r.sendline(to_send)
    r.interactive()

    

    '''
    to_send = int(gmpy2.root(bytes_to_long(payload), 3))
    print(long_to_bytes(to_send ** 3), payload)
    print(to_send)
    '''



def main():
    # Solution:
    # Construct the signature such that it is less than n
    # The value = m^3. The value = the cube root of that which we want to verify
    # When the fake signature is sent, the server will cube the value and take it mod n.
    # It then checks that everything is valid. 
    # We can add garbage values after the payload
    solve()
    # Flag: HTB{4_8131ch3n84ch32_254_vu1n}

if __name__ == '__main__':
    main()
