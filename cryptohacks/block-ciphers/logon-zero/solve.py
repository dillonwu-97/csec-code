from pwn import *
import json
from Crypto.Cipher import AES
from Crypto.Util.number import bytes_to_long
from os import urandom

DEBUG = 0
def reset_password(r, token):
    r.sendline(json.dumps({
        "option": "reset_password",
        "token": token
    }))
    l = r.recvline()
    if DEBUG:
        print(l)

def reset_connection(r):
    r.sendline(json.dumps({
        "option": "reset_connection"
    }))
    l = r.recvline()
    if DEBUG:
        print(l)

def authenticate(r, password):
    r.sendline(json.dumps({
        "option": "authenticate",
        "password": password
    }))
    l = r.recvline()
    if DEBUG:
        print(l)
    return l

def exploit():
    p = remote('socket.cryptohack.org', 13399)
    p.recvline()
    iv = '00' * 16
    password = '00' * 12
    length = '00' * 3
    payload = iv + password + length + '00'
    assert(len(payload) == 64)
    for i in range(1000):
        reset_password(p, payload) # I think this needs to be in the loop because the challenge instance is regenerated every time
        reset_connection(p)
        has_flag = authenticate(p, '\x00' * 0)
        print(f'{i}, {has_flag}')
        if b'Wrong' not in has_flag:
            print(has_flag)
            break

def main():
    exploit()
    # Flag: crypto{Zerologon_Windows_CVE-2020-1472}

if __name__ == '__main__':
    main()