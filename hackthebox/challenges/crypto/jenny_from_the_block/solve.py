from pwn import *
from hashlib import sha256


BLOCK_SIZE = 32
def decrypt_block(enc_block, secret):
    '''
    secret shuld be the digest
    '''
    print(enc_block, secret)
    dec_block = b''
    val = None
    for i in range(BLOCK_SIZE):
        if (enc_block[i] >= secret[i]):
            val = enc_block[i] - secret[i]
            #val = int.from_bytes(enc_block[i], "big") - int.from_bytes(secret[i], "big")
        else:
            val = enc_block[i] + 256 - secret[i]
            #val = int.from_bytes(enc_block[i], "big") + 256 - int.from_bytes(secret[i], "big")
        dec_block += bytes([val])
    return dec_block
    

def encrypt_block(block, secret):
    enc_block = b''
    # for each i in the size of the block, add the values and mod 256 
    for i in range(BLOCK_SIZE):
        val = (block[i]+secret[i]) % 256
        enc_block += bytes([val])
    return enc_block

def main():
    ciphertext = '593e52405d53ebd799f675d3da52d313ac7a92adc8e90a254b01f19543cfbaec8bc185bc92f82e56293b730ff949f517248a333e80a64ce2f461bb325900b93a1dcf23bb2f5d90858a927338c130d3f5594cc14b5ac384e1f8c79603aeda9461045fde08f153037c4823a7ea5be337b8cf2f86fabbe1e23b86942ec476d64975fb379381d4a20fa9fc9c2c3f34ebe3fdc57aac5aa2304f0ae40ff645445051ea7c8312fe5d38fb66b94b3eea527f375aa0d0f9c2ed8df9bdebc52c90e5767f685121c7d26ae0a56e5fa3c922336ba615066e2986faa61b29fefbae40eca886985e79fad340ef71b57888ddd8eef21f946cc8a10a2f06dc24905836d9dc8fddd0'
    c = bytes.fromhex(ciphertext)
    assert (len(c) % BLOCK_SIZE == 0)
    enc_blocks = [c[i:i+BLOCK_SIZE] for i in range(0, len(c), BLOCK_SIZE)]
    # for each enc_block in enc_blocks, get the sha256 value

    p1 = b'Command executed: cat secret.txt'
    h = sha256(enc_blocks[0] + p1).digest()

    for i,enc_block in enumerate(enc_blocks):
        if i == 0: continue
        dec_block = decrypt_block(enc_block, h)
        h = sha256(enc_block + dec_block).digest()
        print(dec_block)



    # "Command executed" <-- 16 bytes
    # ": cat secret.txt" <-- 16 bytes

    # flag: HTB{th1s_b451c_b107k_c1ph3r_1s_n0t_s@fe}

if __name__ == '__main__':
    main()
