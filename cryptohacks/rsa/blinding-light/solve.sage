from pwn import *
from requests import *
import json
from Crypto.Util.number import *

ADMIN_TOKEN = b"admin=True"
r = remote('socket.cryptohack.org', 13376)

def sandbox():
    N = getPrime(256) * getPrime(256)
    val = getPrime(256)
    d = 100
    temp = pow( pow(val, 2, N), d, N)
    #assert (pow(temp, 1/2, N) == pow(val, d, N))
    print(isPrime(bytes_to_long(ADMIN_TOKEN)))
    print(factor(bytes_to_long(ADMIN_TOKEN)))
    


def solve():
    r.recvline()
    pk = json.dumps({"option":"get_pubkey"}).encode()
    r.sendline(pk)

    l = r.recvline()
    pk = json.loads(l.decode())
    n = int(pk['N'][2:],16)
    e = int(pk['e'][2:],16)
    assert e == 0x10001
    
    f = factor(bytes_to_long(ADMIN_TOKEN))
    a = f[0][0]
    b = f[1][0]
    #print(bytes_to_long(bytes.fromhex(a.hex())), int(a))
    print(b)
    assert (bytes_to_long(bytes.fromhex("0" + b.hex())) == int(b))
    print("[*] Factored")

    payload = {"option": "sign", "msg": a.hex()}
    payload = json.dumps(payload).encode()
    r.sendline(payload)
    l = r.recvline()
    sig_resp = json.loads(l.decode())
    sig_a = int(sig_resp['signature'][2:], 16)

    payload = {"option": "sign", "msg": "0" + b.hex()}
    payload = json.dumps(payload).encode()
    r.sendline(payload)
    l = r.recvline()
    sig_resp = json.loads(l.decode())
    sig_b = int(sig_resp['signature'][2:], 16)
    
    to_send = (sig_a * sig_b) % n
    to_send = hex(to_send)[2:]
    print(len(to_send), to_send)

    payload2 = {"option": "verify", "signature": to_send, "msg":ADMIN_TOKEN.hex()}
    p2 = json.dumps(payload2).encode()
    r.sendline(p2)
    l = r.recvline()
    print(l)

def main():
    solve()
    #sandbox()
    # flag: crypto{m4ll34b1l17y_c4n_b3_d4n63r0u5}

if __name__ == '__main__':
    main()
