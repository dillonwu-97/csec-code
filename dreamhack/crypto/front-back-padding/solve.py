from pwn import *
from Crypto.Util.number import bytes_to_long, long_to_bytes

def xor(a, b):
    assert len(a) == len(b)
    ret = ''
    for i in range(0,32, 2):
        ret += hex(int(a[i:i+2], 16) ^ int(b[i:i+2], 16))[2:].zfill(2)
    return ret

def main():

    LOCAL = False
    if LOCAL:
        r = process('./prob.py')
        true_iv = r.recvline().decode().strip()
        print("iv: ", true_iv)
    else:
        r = remote('host3.dreamhack.games', 15301)


    l = r.sendlineafter("> ", "3")
    l = r.recvline()
    enc_flag = r.recvline().decode().split(":")[1].strip()
    assert len(enc_flag) % 32 == 0
    print(f"Encrypted flag: {enc_flag}")

    # step 1:
    payload1 = "k_prefixhappy_Am"
    r.sendlineafter("> ", "1")
    print(payload1.encode().hex())
    r.sendlineafter("> ", payload1.encode().hex())
    enc_prefix = r.recvline().decode().split(": ")[1].strip()
    assert len(enc_prefix) == 64
    print("prefix is: ", enc_prefix)
    ct_1 = enc_prefix[0:32] # encrypted with the iv and used for xor with pt_2
    ct_2 = enc_prefix[32:64]
    pt_1 = b'DreamHack_prefix'.hex()
    pt_2 = b'happy_Amo_suffix'.hex()

    # step 2: Decrypt ct_1 to get garbled plaintext 
    payload2 = ct_1 + ct_1 + ct_2
    r.sendlineafter("> ", "2")
    r.sendlineafter("> ", payload2)
    if LOCAL:
        l = r.recvline()
        print("pt: ", l)

    l = r.recvline().decode().split(": ")[1].strip()
    print("payload2 dec: ", l)

    interm = xor(ct_1, l)
    print("intermediate: ", interm)
    iv = xor(interm, pt_1)
    print("iv: ", iv)

    #step 3:
    payload3 = ct_1 + iv + enc_flag + ct_2 + ct_2
    assert len(payload3) % 32 == 0
    print("payload3: ", payload3)
    r.sendlineafter("> ", "2")
    r.sendlineafter("> ", ct_1 + ct_1 + iv + enc_flag + ct_1 + ct_2)
    if LOCAL:
        l = r.recvline()
        print("pt: ", l)

    l = r.recvline().decode().split(": ")[1].strip()
    flag = ''
    for i in range(0, len(l), 2):
        flag += chr(int(l[i:i+2], 16))
    print("flag: ", flag)


if __name__ == '__main__':
    main()
    # flag: DH{f49e50ad504acfa59ba8333bc1f5b84a172ea5881217a9ccee9fd48bc467a41f}
