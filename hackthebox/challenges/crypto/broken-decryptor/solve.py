from Crypto.Util.number import bytes_to_long, long_to_bytes
from pwn import *
import numpy as np

LOCAL = False
if LOCAL:
    r = remote('localhost', 1337)
else:
    r = remote('167.172.61.89',32028)

FLAG_LEN = 15

def get_encryptor(pt, ct):
    '''
    Get the encryptor for CTR mode
    The encryptor will be used to xor with the ciphertext of the flag to get the plaintext
    The encryptor is recovered because we know both the plaintext and ciphertext of some message
    '''
    assert(len(pt) == len(ct))
    print(pt, ct)
    return bytes([a^b for a,b in zip(pt, ct)])

    

def flag_cipher():
    '''
    Get the ciphertext for the flag
    '''
    r.recvuntil(": ")
    r.sendline("1")
    c = r.recvline().decode().strip('\n')
    return c

def my_cipher(pt):
    '''
    Get the ciphertext for my input
    '''
    r.recvuntil(": ")
    r.sendline("2")
    r.recvuntil(": ")
    r.sendline(pt)
    ct = r.recvline().decode().strip('\n')
    return ct

def build_freq(mode, my_pt = None):
    '''
    There is a lack of randomness for the one time pad
    The frequency of 0xff bytes is greater than other bytes
    With enough requests, we can build a frequency graph
    '''

    # row = character, column = letter
    freq_graph = [[0 for i in range(256)] for i in range(FLAG_LEN)]
    
    for i in range(15000):
        if (i % 100 == 0): print("Iteration: ", i)
        if (mode == 'flag'):
            c = flag_cipher()
        elif (mode == 'mine'): 
            c = my_cipher(my_pt)
        for i in range(0, len(c), 2):
            num = int(c[i:i+2], 16)
            freq_graph[i // 2][num] += 1

    ret = b''
    for i in range(len(freq_graph)):
        ret += int.to_bytes(int(np.argmax(freq_graph[i])), 1, byteorder='little')
        # print("i: ", i, int(np.argmax(freq_graph[i])), freq_graph[i][int(np.argmax(freq_graph[i]))])

    return ret

def solve():
    otp = b'\xff' * FLAG_LEN

    print("[*] Getting encryptor")
    my_pt = 'aa' * FLAG_LEN
    otp_my_ct = build_freq('mine', my_pt = my_pt)
    my_ct = bytes([a ^ b for a,b in zip(otp_my_ct, otp)])
    encryptor = get_encryptor(bytes.fromhex(my_pt), my_ct)
    print(encryptor)

    # Checking
    # my_pt = 'bb' * FLAG_LEN
    # otp_my_ct = build_freq('mine', my_pt = my_pt)
    # my_ct = bytes([a ^ b for a,b in zip(otp_my_ct, otp)])
    # check = get_encryptor(bytes.fromhex(my_pt), my_ct)
    # print(check, encryptor)
    
    print("[*] Retrieving flag")
    otp_flag = build_freq('flag') # get the values which correspond to the ciphertext being xored with the value 0xff
    flag_ct = bytes([a ^ b for a,b in zip(otp_flag, otp)])
    flag_pt = bytes([a ^ b for a,b, in zip(encryptor, flag_ct)])
    print(flag_pt)
        
    


def main():
    solve()
    # Flag: HTB{1V_r3u$3#!}

if __name__ == '__main__':
    main()