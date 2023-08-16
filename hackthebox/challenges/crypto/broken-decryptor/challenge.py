#!/usr/bin/python3
import socketserver
from Crypto.Cipher import AES
from Crypto.Util import Counter
import os

key = os.urandom(0x10).replace(b'\x00', b'\xff')
iv = os.urandom(0x10).replace(b'\x00', b'\xff') # iv is random 

def xor(a, b):
    return bytes([_a ^ _b for _a, _b in zip(a, b)])

def unhex(msg):
    return bytes.fromhex(msg)

# is this creating a new counter each time? 
def encrypt(data):
    ctr = Counter.new(128, initial_value=int(iv.hex(), 16)) # create a 128 bit counter
    crypto = AES.new(key, AES.MODE_CTR, counter=ctr) # new aes key
    if type(data) != bytes:
        data = data.encode()
        # print("data: ", data)
    otp = os.urandom(len(data)).replace(b'\x00', b'\xff') # what happens if I just send 0 bytes over? this seems kind of weird
    # Maybe I lost the one time pad?
    # print("otp: ", otp, crypto.encrypt(data)) # there is also no padding interestingly
    # Can i leak the one time pad somehow? 
    return xor(crypto.encrypt(data), otp)

    # Let's see what happens when there is no otp
    # When there is no otp, the message returned is the exact same since the counter resets each time
    # return crypto.encrypt(data)

# ctr mode
def decrypt(data):
    print("Decrypting")
    ctr = Counter.new(128, initial_value=int(iv.hex(), 16))
    crypto = AES.new(key, AES.MODE_CTR, counter=ctr)
    print(ctr, crypto)
    print(data)
    print(data.encode()) # data is already in bytes so data.encode() will fail

    print(crypto.decrypt(data.encode()))
    return crypto.decrypt(data.encode())

def get_flag():
    # flag = open('flag.txt', 'r').read().strip()
    flag = 'c' * 15
    return encrypt(flag)

def send_msg(s, msg):
    s.send(msg.encode())

def get_input(s, msg):
    send_msg(s, msg)
    data = b''
    while (recv := s.recv(0x1000)) != b'':
        data += recv
        if data.endswith(b'\n'):
            break
    data = data.strip()
    return data.decode()

def main(s):
    while True:

        # I can get the flag
        # I can encrypt any message I want
        # I can decrypt a message
        send_msg(s, '1) Get flag\n')
        send_msg(s, '2) Encrypt Message\n')
        send_msg(s, '3) Decrypt Message\n')
        try:
            opt = get_input(s, 'Your option: ')
            if opt == '1':
                send_msg(s, get_flag().hex()+'\n')
            elif opt == '2':
                pt = get_input(s, 'Enter plaintext: ')
                send_msg(s, encrypt(unhex(pt)).hex()+'\n')
            elif opt == '3':
                ct = get_input(s, 'Enter ciphertext: ')
                # print("ct: ", ct)
                send_msg(s, decrypt(unhex(ct)).hex()+'\n')
            else:
                send_msg(s, 'Invalid option!\n')
        except:
            send_msg(s, 'An error occured.')
            return

class Handler(socketserver.BaseRequestHandler):
    def handle(self):
        main(self.request)

if __name__ == '__main__':
    socketserver.ThreadingTCPServer.allow_reuse_address = True
    server = socketserver.ThreadingTCPServer(('0.0.0.0', 1337), Handler)
    server.serve_forever()
