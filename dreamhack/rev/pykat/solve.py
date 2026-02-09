from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
from scapy.all import *
import zipfile
from hashlib import sha1
import random

FILENAME = './packet.pcapng'
packets = rdpcap(FILENAME)
stream_data = []
stream_data_len = []

def extract_result():

    streams = {}
    for pkt in packets:
        if TCP in pkt and Raw in pkt:
            ip = pkt[IP] if IP in pkt else pkt[IPv6]
            key = (
                ip.src, ip.dst, pkt[TCP].sport, pkt[TCP].dport
            )
            streams.setdefault(key, b"")
            streams[key] += bytes(pkt[Raw])

# Search for HTTP POST bodies in each stream
    for stream_id, data in streams.items():
        if b"POST /u HTTP/1.1" in data:
            try:
                # Split headers and body
                headers, body = data.split(b"\r\n\r\n", 1)

                # Optional: Extract Content-Length to ensure we trim the body
                m = re.search(rb'Content-Length: (\d+)', headers)
                if m:
                    length = int(m.group(1))
                    post_body = body[:length]
                    print(f"[*] Extracted POST body ({length} bytes)")
                    if length not in stream_data_len:
                        stream_data_len.append(length)
                        stream_data.append(post_body)

                # Write the POST body to a file
            except Exception as e:
                print(f"[!] Failed to extract POST body: {e}")

def decrypt(key, ct):
    key = pad(key, 16)
    cipher = AES.new(key, AES.MODE_ECB)
    pt = cipher.decrypt(ct)
    return pt

def zip_stuff(to_zip):
    b = io.BytesIO()
    zf = zipfile.ZipFile(b, mode='w')
    zf.writestr('secure_dump', to_zip)
    zf.close()
    open('dump.zip', 'wb').write(b.getbuffer())

def main():
    extract_result()
    for i,v in enumerate(stream_data):
        print(v.hex())
        print(len(v))

    key = b'wane_is_god'
    print(decrypt(key, stream_data[0]).decode())

    exe_file_maybe = decrypt(key, stream_data[1])
    f = open('./secure_dump', 'wb')
    f.write(exe_file_maybe)
    f.close()

    # key = b'wane_is_noob'
    # result = decrypt(key, stream_data[-1])
    # f = open('./result', 'wb')
    # f.write(result)
    # f.close()
    #
def rev_id_leak():
    '''
    Leak some information first
    we also need to be within the ascii range
    i think there are secondary swaps so need to handle this
    okay, we know that the first value is correct so now we can just reverse in forward direction
    '''
    char_arr = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!#%&()*+-;<=>?@^_`{|}~'
    id_str = '2CPGAnU4%FO5HB6VT09m3'
    id_str_rev = id_str[::-1]
    test_val = ''
    for i,v in enumerate(id_str):
        pos = char_arr.index(v) 
        if pos < 33:
            pos += 0x55
        chr_val = chr(pos)
        print(chr_val)
        test_val += chr_val
    # test_val = test_val[::-1]
    print(test_val)

def rev_id():
    start_chars = 'Wane_1s'
    char_arr = list('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!#$%&()*+-;<=>?@^_`{|}~')
    id_str = '2CPGAnU4%FO5HB6VT09m3'
    ret = start_chars # return value
    for i,v in enumerate(id_str):
        cur_pos = 0
        if i < len(start_chars):
            cur_pos = ord(start_chars[i]) % 0x55
        else: # we need to find our next position based on the final output
            for j in range(len(char_arr)):
                if char_arr[j] == id_str[i]: # found a match
                    print(id_str[i], char_arr[j], i, j)
                    cur_pos = j % 0x55
                    if j <= 32:
                        ret += chr(j + 0x55)
                    else:
                        ret += chr(j)
                    break
        print(cur_pos)
        # swap
        temp = char_arr[cur_pos] 
        char_arr[cur_pos] = char_arr[i]
        char_arr[i] = temp
        print(''.join(char_arr))
    print(ret)


def get_four(to_find):
    cur = ''
    print("to find: ", to_find)
    if type(cur) != str:
        to_find = to_find.decode()
    for i in range(32, 128):
        print(i)
        for j in range(32, 128):
            for k in range(32, 128):
                for l in range(32, 128):
                    cur = chr(i) + chr(j) + chr(k) + chr(l)
                    cur = cur.encode()
                    sha1 = hashlib.sha1()
                    sha1.update(cur)
                    d = sha1.hexdigest()
                    # if cur == b'aaaa':
                    #     print(cur)
                    #     print(d)
                    #     input()

                    # print(d, len(d))
                    # print(to_find, len(to_find))
                    assert type(d) == type(to_find)
                    if d == to_find:
                        input("Found!")
                        return cur.decode()

def rev_pass():
    # special parameter on the third field
    # spec is if the hex we are looking at is not of length 40 
    def xor_hash(a, b, spec):
        if spec == True:
            # this was for second hash
            # print("remove character: ", hex(b[32]))
            # b = b[:32] + b[32+1:]

            # for the third hash
            # a = a[:32] + a[32+1:]
            
            # for the fourth hash
            # b = b[:28] + b[28+1:]
            # b = b[:34] + b[34+1:]

            # for the fifth hash
            # a = a[:30] + a[30+1:]
            # a = a[:32] + a[32+1:]

            # for the sixth hash
            b = b[:31] + b[31+1:]
            pass


        # assert len(a) == len(b)
        ret = ''
        print(a, b)
        print(len(a), len(b))
        for i in range(min(len(a), len(b))):
            temp = a[i] ^ b[i]
            if (chr(temp) == '<'):
                print("pause: ", i, b[i], chr(b[i]))
                input()
            ret += chr(temp)
        return ret

    f = open('./result', 'rb').read()
    # f = open('./dummy_res', 'rb').read()
    all_chunks = f.split(b'\xff')
    pass_chunks = all_chunks[1:-1]
    for i in pass_chunks:
        print(len(i.hex()))

    # print(get_four(pass_chunks[0], None))
    # to_use = '6ff44ddab66a9543aa2390df052cbe5b9a446460'.encode()
    test_2 = xor_hash(pass_chunks[4], pass_chunks[5], True)
    print(test_2)
    # print(get_four(test_2))
    pass

def part_3_mersenne():
    keys = open('./mersenne_bytes', 'r').read().split('\n')
    k = []
    for i in keys:
        if "eax:" in i:
            temp = i.split("eax: ")[1]
            # print("val: ", int(temp,16))
            k.append(int(temp,16))
    assert len(k) == 64

    f = open('./result', 'rb').read()
    all_chunks = f.split(b'\xff')
    last_chunk = all_chunks[-1]
    print(len(last_chunk))
    print(k)
    flag = ''
    for i in range(len(k)):
        temp = k[i] ^ last_chunk[i]
        print(chr(temp))
        flag += chr(temp)
    print(flag)

    # flag: DH{===T0P_S3CR37===|WAnE_10v35_n4k1R1_4y4ME|===T0P_S3CR37===}

if __name__ == '__main__':
    # main()
    # rev_id()
    # rev_pass()
    part_3_mersenne()
