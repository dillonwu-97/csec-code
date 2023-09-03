from pwn import *
from ast import literal_eval
from Crypto.Util.number import getPrime, isPrime
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib
# Helpful Links:
# https://crypto.stackexchange.com/questions/87924/how-to-reconstruct-the-static-private-key-of-a-diffie-hellman-client-when-i-can
# For finding primes
# https://crypto.stackexchange.com/questions/22716/generation-of-a-cyclic-group-of-prime-order
# Attack idea:
# small subgroup attack
# Step 1: Identify the size of the prime p
# Step 2: Construct a prime p s.t. (p-1) is n-smooth
# Step 3: Find a nontrivial generator for one of the subgroups of (p-1)
# Step 4: Send nontrivial generator g, and prime p to Bob 
# Step 5: Solve diffie hellman problem for the small subgroup to recover Bob's secret key using B


r = remote('socket.cryptohack.org', 13373)

'''
def construct_smooth_num():
    primes = []
    p = 1
    for i in range(49):
        r = getPrime(32)
        primes.append(r)
        p *= r
    primes.append(2)
    return 2*p+1,primes
'''


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

def construct_bad_num():
    p = getPrime(1024) 
    q = getPrime(512)
    ret = 1
    while 1:
        r = getPrime(42)
        ret = 2 * (r * p * q) + 1
        if isPrime(ret):
            print("p: {p}\nq: {q}\nr: {r}\n")
            break
    return ret, [r,p,q,2]

def construct_generator(my_num, primes):
    h = getPrime(42)
    prod = 1
    for i,v in enumerate(primes):
        if i == 0: continue
        prod *= v
    assert (prod * primes[0] + 1) == my_num

    g = 1
    while 1:
        g = pow(h, prod, my_num)
        if g != 1:
            break
    return g

def solve():
    alice = literal_eval(r.recvline().decode().strip('\n').split("Alice: ")[1])
    bob = literal_eval(r.recvline().decode().strip('\n').split("Bob: ")[1])
    alice2 = literal_eval(r.recvline().decode().strip('\n').split("Alice: ")[1])

    p_orig = int(alice['p'][2:], 16)
    g_orig = 2
    A_orig = int(alice['A'][2:], 16)
    B_orig = int(bob['B'][2:], 16)
    iv = alice2['iv']
    enc = alice2['encrypted']

    print(alice)
    print(bob)
    print(alice2)

    p_size = len(bin(p_orig)[2:])
    print("Prime size: ", p_size)

    my_num, primes = construct_bad_num() # 1548 bit prime
    print("Bitlength: ", len(my_num.bits()))
    assert my_num > p_orig
    assert isPrime(my_num)
    print("My constructed prime: ", my_num)

    g = construct_generator(my_num, primes)
    print(f"[*] Found a bad generator for {my_num} in subgroup {primes[0]}: {g}")

    fake_A = 0x1

    print('[*] Sending to Bob')
    payload = '"p": "{my_num}", "g": "{gen}", "A": "{A}"'.format(my_num = hex(int(my_num)), gen = hex(int(g)), A = hex(fake_A))
    #payload = '"p": "{my_num}", "g": "{gen}"'.format(my_num = hex(int(my_num)), gen = hex(int(g)))
    payload = "{" + payload + "}"
    print(payload)
    r.sendline(payload)
    # l = r.recvline()
    # print(l)
    # input()
    bob2 = literal_eval(r.recvline().decode().strip('\n').split("you: ")[1])
    B = int(bob2["B"][2:],16)
    print("[*] Received B from Bob")
    print(f"B: {B}")

    # # Solving for Bob's secret key using diffie hellman
    R = IntegerModRing(my_num)
    print(g, B)
    g_in_R = R(g)
    B_in_R = R(B)
    b = discrete_log(B_in_R, g_in_R, ord=ZZ(primes[0]))
    assert pow(g,b ,my_num) == B

    ss = int(pow(A_orig,b,p_orig))
    print(f"[*] Found Bob's secret key: {b}")

    print(p_orig)
    print("Trying: ", pow(g_orig, b, p_orig))
    print("B orig: ", B_orig)
    # assert (p_orig >= pow(g_orig,b, p_orig)) # it's weird that this fails; should check it out
    # assert pow(g_orig, b, p_orig) == B_orig

    print(decrypt_flag(ss, iv, enc))

def solve2():
    alice = literal_eval(r.recvline().decode().strip('\n').split("Alice: ")[1])
    bob = literal_eval(r.recvline().decode().strip('\n').split("Bob: ")[1])
    alice2 = literal_eval(r.recvline().decode().strip('\n').split("Alice: ")[1])

    p_orig = int(alice['p'][2:], 16)
    g_orig = 2
    A_orig = int(alice['A'][2:], 16)
    B_orig = int(bob['B'][2:], 16)
    iv = alice2['iv']
    enc = alice2['encrypted']


    print('[*] Sending to Bob')
    fake_A = 0x1
    payload = '"p": "{my_num}", "g": "{gen}", "A": "{A}"'.format(my_num = hex(p_orig), gen = hex(A_orig), A = hex(fake_A))
    payload = "{" + payload + "}"
    print(payload)
    r.sendline(payload)

    bob2 = literal_eval(r.recvline().decode().strip('\n').split("you: ")[1])
    ss = int(bob2["B"][2:],16)
    print(decrypt_flag(ss, iv, enc))
    print("[*] Received B from Bob")
    # Flag: crypto{n07_3ph3m3r4l_3n0u6h}

def main():
    solve2()

if __name__ == '__main__':
    main()
