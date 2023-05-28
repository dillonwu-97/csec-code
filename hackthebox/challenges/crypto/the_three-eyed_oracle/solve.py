from pwn import *
from base64 import *
from requests import *
#from Crypto.Util.Number import bytes_to_long, long_to_bytes

class Solver:
    # r is remote
    # p is port
    def __init__(self, url=None, port=None):
        self.url = url
        self.port = port
        self.r = None
        print(url, port)
        if url != None and port != None:
            self.r = remote(url, port)
    
    # send payload
    def sp(self, payload):
        self.r.recvuntil(">")
        self.r.sendline(payload)
        l = self.r.recvline()
        return l.strip()

    def split_block(self, ciphertext):
        blocks = []
        for i in range(0, len(ciphertext), 32):
            blocks.append(ciphertext[i:i+23])
        return blocks

# pseudocode:
# grab the correct ciphertext first 
# for each character 
#   construct a new payload and send to the remote host
#   payload is equal to the  
def solve():
    solver = Solver("68.183.34.87", 30328)
    payload_size = 4 + 32 - 1 # 4 to pad the prepend, 16 is the size of the block, 1 for the first character
    flag = ''
    sflag = ''
    for i in range(payload_size, 0, -1):
        payload = 'aa' * payload_size
        correct_blocks = solver.split_block(solver.sp(payload))
        print(correct_blocks)
        for i in range(33, 127):
            guess = payload + flag + hex(i)[2:].zfill(2)
            guess_blocks = solver.split_block(solver.sp(guess))
            print(guess, correct_blocks[1], guess_blocks[1])
            if correct_blocks[2] == guess_blocks[2]:
                flag += hex(i)[2:].zfill(2)
                sflag += chr(i)
                print(flag, sflag)
                break
        payload_size -=1
    print(sflag)



def main():
    print("[*] Starting solve")
    solve()
    # Flag: HTB{7h3_br0k3n_0r@c1e!!!}

if __name__ == '__main__':
    main()


