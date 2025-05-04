# v8 = a                                    
#          ^ (a ^ b )
#          & f ;

from ctypes import CDLL
from scapy.all import TCP,rdpcap
import base64
from Crypto.Cipher import AES

def first_transform(a):

    b = a - ord('W')
    c = a - ord('a')
    d = ord('f') - a
    e = (c | d) >> 31
    f = e - 1
    ret = a ^ (a ^ b) & f
    return ret % 0xff


def sec_transform(a, b, start):
    #   *next_char_to_look_at |= (((unsigned __int8)b
    #                            ^ (b
    #                             ^ (unsigned __int8)(a - '\a'))
    #                            & (unsigned __int8)f
    #                           & 0xF) << (4 * (start & 7));
    # c = ord('F' - )
     
    c = ord('F') - a
    d = a - ord('A')
    e = int((c | d) < 0)
    f = e - 1

    g = a - ord('\a')
    # i think this cancels out the b xor but whatever, it's what the code says
    h = g ^ b
    i = b ^ h & f

    j = i & 0xF
    k = j << (4 * (start & 7))
    return k


def sandbox1():
    start = 0 # not sure how much this affects 
    for i in range(0x0, 0xff):
        first = first_transform(i)
        print(f"first: {hex(i)}, {hex(first)}")

        second = sec_transform(first, i, 0)
        print(f"second with static {start}: {hex(i)}, {hex(second)}")


def grab_data():
    f = rdpcap('./dump.pcap')
    data = b''
    sessions = f.sessions()
    for session_key, session_pkts in sessions.items():
        for pkt in session_pkts:
            data += bytes(pkt[TCP].payload)
    return data[:47104]

def find_key_vert(try_val):
    # libc = CDLL("libc.so.6")
    libc = ("msvcrt.dll")
    libc.srand(try_val)
    to_check = b'\x57\xbf\xce\x56\x3c'
    data = list(to_check)
      
    for i in range(len(to_check)):
        val = libc.rand() & 0xff
        data[i] ^= val

    ret = ''.join([chr(i) for i in data])
    print(ret)
    if ret == 'SQLit':
        input("Found!")

def find_key_hor(try_val,start): # try to move horizontally to find solution
    libc = CDLL("libc.so.6")
    libc.srand(try_val)
    to_check = grab_data()[4096:][start:start+5]
    assert len(to_check) == 5
    # print(to_check, start)
    data = list(to_check)
      
    for i in range(len(to_check)):
        val = libc.rand() & 0xff
        data[i] ^= val

    print(data)
    ret = ''.join([chr(i) for i in data])
    # print(ret)
    if 'SQL' in ret:
        input("Found!")

def sandbox(try_val):
    libc = CDLL("libc.so.6")
    # filesize = 47104
    filesize = try_val
    print(f"filesize {filesize}")
    libc.srand(filesize)
    data = grab_data()
    assert len(data) == 47104
    first_chunk = data[:4096]
    data_vals = list(data[4096:])
   
    for i in range(len(data_vals)):
        # rand has to be correct
        val = libc.rand()
        r = val & 0xff
        # if (i == 0 and r == 106):
        #     input("found")
        # print(data_vals[i], hex(data_vals[i]), val, hex(val))
        data_vals[i] ^= r
        # input()

    ret = ''.join([chr(i) for i in data_vals])

    # print(ret[:100])
    # print(ret)
    ciphertext = b''.join([int.to_bytes(i, byteorder='little',length=1) for i in data_vals])

    b64_key = "8u4orW2bmcHxpJA2HRTdpem0ksiY8kKInf8umZnsLbA="
    key = base64.b64decode(b64_key)
    # print(f"key: {key}")
    assert len(key) == 32

    # i think the tag looks wrong but whatever
    header = ciphertext[:3]
    if header == b'SQL':
        print(ciphertext)
        input("FOUND!")
    iv = ciphertext[3:15]
    payload = ciphertext[15:-16]
    cipher = AES.new(key, AES.MODE_GCM, iv)
    dec = cipher.decrypt(payload)
    print(ciphertext[:10])
    print(dec[:10])
    for i in range(0, len(ciphertext)-3):
        if ciphertext[i:i+5] == b'SQLit':
            print(ciphertext[i:i+3])
            input()
    # print(dec)

def solve():
    # libc = CDLL("libc.so.6")
    libc = CDLL("msvcrt.dll")
    filesize = 47104
    print(f"filesize {filesize}")
    data = grab_data()
    first_chunk = data[:4096]
    data_vals = list(data[4096:])
    assert data_vals[0] == 0x57
    libc.srand(filesize)
   
    for i in range(len(data_vals)):
        val = libc.rand()
        # print(f"val: {val}")
        r = val & 0xff
        data_vals[i] ^= r

    ret = ''.join([chr(i) for i in data_vals])
    sqlite = b''.join([int.to_bytes(i, byteorder='little',length=1) for i in data_vals])
    f = open('./sqlitedata', 'wb')
    f.write(sqlite)
    f.close()

def get_flag():
    f = open('./sqlitedata', 'rb')
    data = f.read()
    print(data)
    enc = data.split(b'flag')[1].split(b'https://dreamhack')[0]
    print(enc)
    b64_key = "8u4orW2bmcHxpJA2HRTdpem0ksiY8kKInf8umZnsLbA="
    key = base64.b64decode(b64_key)
    # print(f"key: {key}")
    assert len(key) == 32
    iv = enc[3:15]
    payload = enc[15:-16]
    cipher = AES.new(key, AES.MODE_GCM, iv)
    dec = cipher.decrypt(payload)
    print(dec)
    # flag: DH{Correct_DAPI_Masterkey_^^!}


def main():
# Step 1:
    # solve()
# Step 2:
    get_flag()
        
    # sandbox()
    # for i in range(0, 47104):
        # print(i)
        # find_key_hor(47104, i)
    # for i in range(1, 1000000):
        # find_key_vert(i)
        # print(i)
        # solve(i)
    #
    # solve(0x41704)
    # find_key(47104)
if __name__ == '__main__':
    main()
