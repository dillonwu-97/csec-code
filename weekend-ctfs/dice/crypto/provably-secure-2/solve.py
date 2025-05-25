from pwn import *

def byte_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

def req_enc(r, e1, e2):
    r.recvuntil('Action: ')
    r.sendline('1')
    r.recvuntil(': ')
    r.sendline(e1)
    r.recvuntil(': ')
    r.sendline(e2)
    enc = r.recvline()
    return enc.decode().strip()

def req_dec(r, to_dec):
    
    r.recvuntil('Action: ')
    r.sendline('2')
    l = r.recvuntil('hexstring): ')
    r.sendline(to_dec)
    dec = r.recvline()
    return bytes.fromhex(dec.decode().strip())

def req_guess(r, guess):
    r.recvuntil(': ')
    r.sendline('0')
    r.recvuntil(': ')
    r.sendline(guess)
    r.recvline()
    # assert ('Correct in l.decode()')

def main():
    r = remote('mc.ax', 31497)
    for i in range(128):
        if i % 8 == 0:
            print("iter: ", i)

        # Send three encryption requests
        m0 = '00' * 16
        m1 = '11' * 16
        m2 = '22' * 16
        m3 = '33' * 16
        m4 = '44' * 16
        m5 = '55' * 16

        enc_one = req_enc(r, m0, m1)
        enc_two = req_enc(r, m2, m3)
        enc_three = req_enc(r, m4, m5)

        # print (len(enc_one), len(enc_two), len(enc_three))
        # print(enc_one, enc_two, enc_three)

        # Send three decryption requests to recover the message
        # [enc_one_first, enc_two_second]
        # [enc_three_first, enc_two_second]
        # [enc_three_first, enc_one_second]
        payload_one = enc_one[:512] + enc_two[512:]
        payload_two = enc_three[:512] + enc_two[512:]
        payload_three = enc_three[:512] + enc_one[512:]
        dec_one = req_dec(r, payload_one)
        dec_two = req_dec(r, payload_two)
        dec_three = req_dec(r, payload_three)
        # print(dec_one, dec_two, dec_three)

        # Get the flag
        guess = (byte_xor(byte_xor(dec_one, dec_two), dec_three))
        if guess == b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00':
            guess = '0'
        else:
            guess = '1'
        req_guess(r, guess)

    l = r.recvline()
    print(l)

if __name__ == '__main__':
    main()
