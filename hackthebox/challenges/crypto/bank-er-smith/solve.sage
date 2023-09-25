from pwn import *
from base64 import *
from requests import *
from Crypto.Util.number import bytes_to_long, long_to_bytes

def sandbox():
    r = remote('209.97.140.29', 30705)
    enc_passphrase = bytes.fromhex(r.recvline().decode().strip('\n').split(": ")[1])
    print(f"enc passphrase is: {enc_passphrase}")
    
    r.recvuntil("> ")
    r.sendline("1")
    r.recvline()
    n = int(r.recvline().decode().strip('\n'))
    e = int(r.recvline().decode().strip('\n'))

    print(f'n: {n}')
    print(f'e: {e}')

    r.recvuntil("> ")
    r.sendline("2")
    l = r.recvline()
    hint = int(r.recvline().decode().strip('\n'))
    print(f'hint: {hint}')

    # F.<x> = PolynomialRing(Zmod(n), names=('x',))
    # x = F._first_ngens(1)[0]
    F.<x> = PolynomialRing(Zmod(n))
    eq = x + hint
    roots = eq.small_roots(2**256, beta=0.5)
    print(f"roots are: {roots}")
    p = int(hint + roots[0])
    print(gcd(p, n))
    assert(roots[0] != n)
    assert (n % p == 0)
    q = n//p
    phi = (q-1) * (p-1)
    d = int(pow(e,-1,phi))
    n = int(n)
    pt = long_to_bytes(pow(bytes_to_long(enc_passphrase),d,n))
    print(f"plaintext: ", pt)

    r.sendline("3")
    r.recvuntil(": ")
    r.sendline("vault_68")
    r.recvuntil(": ")
    r.sendline(pt)
    flag = r.recvline()
    print(flag)
    # Flag: HTB{c00p325m17h_15_57111_m491c!}

    r.interactive()
    # The solution is to use Coppersmith's method to recover bits


def main():
    print("[*] Starting solve")
    sandbox()

if __name__ == '__main__':
    main()


