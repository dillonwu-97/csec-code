from aes_test1 import AES

# 1) xor first character
# 2) move characters around
# 3) xor characters with some keystream <-- most important part
# right, it's not one lbock at a time though, i forgot about that
# def bxor(keystream, block): # use xor for bytes
    # ret = [-1] * 8
    # for i in range(len(keystream)):
    #     temp = block[i % len(block) ] ^  
    #     ret.append(temp) 
    #
    # parts = []
    # for b1, b2 in zip(b1, b2):
    #     parts.append(bytes([b1 ^ b2]))
    # return b''.join(parts)

def shift(chrs):
    arr = [0, 5, 10, 15, 4, 9, 14, 3, 8, 13, 2, 1, 12, 7, 6, 11]
    ret = []
    for i in arr:
        ret.append(chrs[i])
    return ret

def sandbox():
    print(shift("WBch_D]BKXYFWLUJ"))

def main():
    key = open('key.bin', 'rb').read()
    exp= open('expansion.bin', 'rb').read()
    assert len(key) == 16
    assert len(exp) == 176
    nrounds = 10 # 128 bit key should have 10 rounds
    print(key.hex())
    print(exp.hex())

    crypt = AES(key)
    expanded_check = crypt.key_schedule().hex()
    print(expanded_check)
    assert exp.hex() == expanded_check

    crypt = AES(key)
    test_enc = b'ABCDEFGHABCDEFGHABCDEFGHABCDEFGH'
    test_enc = b'ABCDEFGHIJKLMNOPQRSTUVWHYZ12345\n'
    a = crypt.cipher(test_enc[:16]).hex()
    print(crypt.cipher(test_enc[16:32]).hex())
    ab = bytes.fromhex(a)
    print(crypt.inv_cipher(ab))


    # sandbox()



if __name__ == '__main__':
    main()
