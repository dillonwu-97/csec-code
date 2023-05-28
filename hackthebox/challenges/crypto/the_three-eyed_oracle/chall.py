from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import random
import signal
import subprocess
import socketserver

FLAG = b'HTB{--REDACTED--}'
prefix = random.randbytes(12)
key = random.randbytes(16)


def encrypt(key, msg):
    msg = bytes.fromhex(msg)
    crypto = AES.new(key, AES.MODE_ECB)

    # random key is used but it is constant
    # |random 12 bytes | message I send  | flag of unknown length | padding |
    # it's an oracle so just keep sending messages and check if the output of what i guess is the same as the output with the flag in it -> runtime is 256 * length of flag 
    # i think it has to be the last letter though
    # | random 12 bytes | 4 bytes of "aa" | 15 bytes of "aa" | 1 byte letter guess | rest of the flag | <- guess
    # | random 12 bytes | 4 bytes of "aa" | 15 bytes of "aa" | rest of the flag <-- verifier 
    # then iteratively shift to the left so that it becomes 14 bytes of "aa" and my guess 
    padded = pad(prefix + msg + FLAG, 16)
    return crypto.encrypt(padded).hex()


def challenge(req):
    req.sendall(b'Welcome to Klaus\'s crypto lab.\n' +
                b'It seems like there is a prefix appended to the real firmware\n' +
                b'Can you somehow extract the firmware and fix the chip?\n')
    while True:
        req.sendall(b'> ')
        try:
            msg = req.recv(4096).decode()

            ct = encrypt(key, msg)
        except:
            req.sendall(b'An error occurred! Please try again!')

        req.sendall(ct.encode() + b'\n')


class incoming(socketserver.BaseRequestHandler):
    def handle(self):
        signal.alarm(1500)
        req = self.request
        challenge(req)


class ReusableTCPServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass


def main():
    socketserver.TCPServer.allow_reuse_address = True
    server = ReusableTCPServer(("0.0.0.0", 1337), incoming)
    server.serve_forever()


if __name__ == "__main__":
    main()
