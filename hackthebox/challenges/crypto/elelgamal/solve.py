from pwn import *
from base64 import *
from requests import *
from Crypto.Util.number import bytes_to_long, long_to_bytes
import math
from scapy.all import * 

def sandbox():

    # recover s
    enc1 = '43zIOhk1ayUoiAXipAm3tdNPwgyzIhZjRUcRc7fw5PiSUN1b3ICzHEFbNhiti2aB2jdvs4uYHUqN1YdZtyY=|EtJdz4TGpsPRxpCfSU1EzHCdn7dwx/wM5ddhCA4PpiGZTUpytbe6qYbNgrtJNmB3aTGCMiaxFr1jQfjtonk='
    q = 855098176053225973412431085960229957742579395452812393691307482513933863589834014555492084425723928938458815455293344705952604659276623264708067070331
    c1 = bytes_to_long(b64decode(enc1.split("|")[1]))
    m1 = bytes_to_long("Session established".encode())
    m1_inv = pow(m1, -1, q)
    s = (m1_inv * c1) % q
    s_inv = pow(s, -1, q)
    print(s)
    assert((s * m1) % q == c1)

    payloads = []
    packets = rdpcap("./traffic.pcapng")
    for p in packets:
        if p.haslayer(TCP):
            if p[TCP].payload:
                payload = bytes(p[TCP].payload)
                if b'|' in payload:
                    print(payload)
                    payloads.append(payload)
    print(payloads)
    for i,p in enumerate(payloads):
        c = bytes_to_long(b64decode(p.split(b"|")[1]))
        m = (c * s_inv) % q
        print(long_to_bytes(m))


    
    

def main():
    print("[*] Starting solve")
    sandbox()
    # flag: HTB{n3ve2_u53_7h3_54m3_k3y:)}

if __name__ == '__main__':
    main()


