from pwn import *
from base64 import *
from requests import *
import json
from Crypto.Util.number import bytes_to_long, long_to_bytes

def changemode(r, m):

    r.recvuntil('> ')
    r.sendline(json.dumps({
        "option": '3'
    }))

    r.recvuntil(": ")
    r.sendline(json.dumps({
        "modes": m
    }))

def askflag(r):
    r.recvuntil('> ')
    r.sendline(json.dumps({
        "option": '1'
    }))
    l = r.recvline()
    l = r.recvline()
    print(l)
    return l

def sendmsg(r, m):
    r.recvuntil('> ')
    r.sendline(json.dumps({
        "option": "2"
    }))

    r.recvuntil(": ")
    r.sendline(json.dumps({
        "plaintext": m
    }))
    r.recvline()
    r.recvline()
    l = r.recvline()
    print(l)
    return l

def xor(x, y):
    return bytes(a ^ b for a,b in zip(x, y))

def solve():
    LOCAL = False
    if LOCAL:
        r = remote('localhost', 1337)
    else:
        r = remote('157.245.43.189',30773)

    changemode(r, ["CTR"])

    payload = "a" * 64
    l = sendmsg(r, payload)
    msg_enc = json.loads(l)["ciphertext"][:128]
    msg_enc = bytes.fromhex(msg_enc)
    msg_dec = payload.encode()
    encryptor = xor(msg_enc, msg_dec)
    print(encryptor)
    l = r.recvline()
    print(l)
    l = r.recvline()
    print(l)
    flag_enc = json.loads(askflag(r))["ciphertext"]
    print("Flag hex length: ", len(flag_enc)) # 64 byte characters
    flag_enc = bytes.fromhex(flag_enc)
    print(flag_enc)
    print(xor(flag_enc, encryptor))

    # Solution: Exploiting CTR mode, send encrypted message
    # receive encrypted message
    # xor with known plaintext to get the output of the encryption mode 
    # grab flag in CTR mode
    # xor encrypted flag with output of encryption mode
    # get flag






def main():
    print("[*] Starting solve")
    solve()
    # flag: HTB{50_m4ny_m0d35_f02_ju57_4_kn0wn_p141n73x7_4774ck_0n_AES-CTR}

if __name__ == '__main__':
    main()


