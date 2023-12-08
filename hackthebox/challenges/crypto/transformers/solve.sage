from pwn import *
from Crypto.Util.number import isPrime, long_to_bytes, bytes_to_long
import math
import signal
from sage.all import *
import requests
import gmpy2

def timeout_handler(signum, frame):
    raise TimeoutError

def try_factor(pk):
    signal.signal(signal.SIGALRM, timeout_handler)
    try:
        signal.alarm(5)
        f = factor(pk)
        print(f)
        signal.alarm(0)
        return f
    except:
        return "Timeout occurred"

# Observations:
# password is not a prime
# I might need to use wireshark to capture some packets to see what is being communicated
def make_conn():
    r = remote('188.166.175.58', 31116)
    r.recvuntil("Enter the option: ")
    r.sendline('4')
    l = r.recvline().decode()
    pk = int(l.split("KEY: ")[1])
    # print(l)
    l = r.recvline().decode()
    print(l)
    password = int(l.split("PASSWORD: ")[1])

    print(f"public key: {pk}", isPrime(pk)) # public key is not prime
    print(f"password: {password}", isPrime(password)) # password is not prime
    return pk, password

def solve():
    pk2, password2 = make_conn()
    r = remote('188.166.175.58', 31116)
    r.recvuntil("Enter the option: ")
    r.sendline('4')
    l = r.recvline().decode()
    pk1 = int(l.split("KEY: ")[1])
    # print(l)
    l = r.recvline().decode()
    print(l)
    password1 = int(l.split("PASSWORD: ")[1])

    print(f"public key: {pk1}", isPrime(pk1)) # public key is not prime
    print(f"password: {password1}", isPrime(password1)) # password is not prime

        # print(long_to_bytes(pk))
    # print(long_to_bytes(password))

    p  = math.gcd(pk1, pk2) # not factorizable 
    #print("p is: ", p)
    # print(try_factor(pk)) # cannot factor this 
    # print(try_factor(password)) # cannot factor this
    # factordb gives something for the password though:
    a = pk1
    q = a // p
    assert a % q == 0 and a % p == 0
    phi = (p-1) * (q-1)
    #aa =[65537, 3, 17]
    x = 0
    aa = [65537]
    for i in aa:
        try:
            d = gmpy2.invert(i, phi)
            x = long_to_bytes(pow(password1, d, pk1)).decode()
            
        except:
            continue


    print("x: ", x)
    l = r.recvuntil(": ")
    #print(l)
    r.sendline(str(x))
    r.interactive()
'''
    assert int(str(password)) == password
    assert int(str(pk)) == pk
    url = f"http://factordb.com/api"
    r = requests.get(url, params={"query": str(password)}).json()
    print(r)
'''

def main():
    solve()
    # HTB{3uc1id_w4z_th3_pr1me_h4x0r}

if __name__ == '__main__':
    main()
