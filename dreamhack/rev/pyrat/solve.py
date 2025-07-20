from base64 import b64decode
import os 
from Crypto.Cipher import ARC4
import gzip
    
def extract(filename):
    '''
    for each file in the raw directory, grab the png.tmp byte files
    '''
    f = open(filename, 'rb').read()
    payload = f.split(b'\r\n\r\n')[2]
    return payload

def find_mei(filename):
    f = open(filename, 'rb').read()
    # MAGIC = b'MEI\014\013'
    MAGIC = b'MEI'
    for i in range(len(f)-len(MAGIC)):
        if f[i:i+len(MAGIC)] == MAGIC:
            print("Found something that might be extractable", i)
            print(f[i:i+64])
            print(f[i:i+64].hex())
            input()

PATH = './Packet/raw/'
def solve(filename, ctr):
    token='YupD7Z7CU9vazPRG7ZkPE0ykZxIj5YkfRwo8J9WA00qQxXjgxsV6V'
    bot_id = 'IUKASAMJJSHUJBES'
    key = bytes([ord(token[i]) ^ ord(bot_id[i]) for i in range(len(bot_id))])
    assert len(key) == 16

    print(f"token: {token}")
    print(f"bot id: {bot_id}")
    print(f"key: {key}")
    rc4 = ARC4.new(key)

    # data = extract_json(filename)
    data = extract(filename)
    # assert len(data) == 379
    # data = gzip.decompress(data)
    # print("decompressed: ", data)

    print(data.hex())
    input()
    data = rc4.decrypt(data)
    print(data.hex())
    input()
    f2 = open('test_file' + str(ctr), 'wb') 
    f2.write(data)
    f2.close()


def main():
    # filename = PATH + '32_s.txt'
    # extract_png(filename)
    #
    # extract_png(filename)

    # malware_file = './pyrat-malware-dont-bop-me-soc-pls.txt'
    # find_mei(malware_file)
    # files = [
    #     "04_c.txt",
    #     "08_c.txt",
    #     "12_c.txt",
    #     "19_c.txt",
    #     "21_c.txt",
    #     "28_c.txt",
    #     "30_c.txt",
    # ]
    files = [
        '37_c.txt'
    ]
    for i in range(len(files)):
        filename = PATH + files[i]
        data = solve(filename, i)


if __name__ == '__main__':
    main()
DH{B@ckd00r_w1th_PCL0UD!!}
