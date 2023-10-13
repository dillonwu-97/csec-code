from pwn import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode
import zlib

def crc32(inp: bytes):
    #return zlib.crc32(inp) & 0xFFFFFFFF
    return zlib.crc32(inp)

def decrypt(key, iv, msg):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(msg), AES.block_size)


def main():
    a = open('./iv.png', 'rb').read()
    b = open('./ps.png', 'rb').read()

    iv = "abcdefghijklmnop".encode()
    c2 = "https://flare-on.com/evilc2server/report_token/report_token.php?token="
    w1 = "wednesday"
    key = c2[4:10] + w1[2:5]
    crc = str(crc32(key.encode()))
    crc += crc
    key = crc[:16].encode()

    print(f"key: {key}")
    print(f"iv: {iv}")
    dec_a = decrypt(key, iv, a)
    f = open("temp_a", "wb")
    f.write(dec_a)
    f.close()
    
    dec_b = decrypt(key, iv, b)
    f = open("temp_b", "wb")
    f.write(dec_b)
    f.close()
    # Y0Ur3_0N_F1r3_K33P_601N6@flare-on.com

if __name__ == '__main__':
    main()
