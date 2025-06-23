# 0x7fffffffe230: 0x1f6d5e4391523728      0x612270554694793a
# 0x7fffffffe240: 0x73644967583d8b7c      0x00765b4c6a4f408e
#
def rev_hex(s):
    ret = [s[i:i+2] for i in range(len(s)-2,-2,-2)]
    return ''.join(ret)

# v is what we want
def forward(v, xor_val):
    for i in range(33,129):
        temp = (i + 5) & 0xff
        temp = (temp ^ xor_val) % 256
        _temp = temp
        temp = (temp + temp) % 256
        temp = (_temp + temp) % 256
        temp = (temp + 7) % 256
        if v == temp:
            return i
    return 32

def p_add(a, b):
    added_val = 0
    ctr = 0
    while (a):
        temp = ((b & 0xff) + (a & 0xff)) % 256 << (ctr * 8)
        added_val += temp
        b = b >> 0x8
        a = a >> 0x8
        ctr += 1
    return added_val

def p_xor(xor_val, added_val):
    ctr = 0
    while (ctr < 16):
        temp = ((added_val >> (ctr * 8)) & 0xff) << (ctr * 8)
        xor_val ^= temp
        ctr += 1
    return xor_val

def forward_in_first_branch(user_input, xor_val):
    val = 0x05050505050505050505050505050505 # 16 5's
    user_cp = user_input
    added_val = p_add(val, user_cp)
        
    print(hex(added_val)) # is ok
    xor_val = 0x5C5B5A595857565554535251504F4E4D
    xor_val = p_xor(xor_val, added_val)
        # added_val = val + user_input
    # then xor with above value
    print(hex(xor_val))

    val = 0x7070707070707070707070707070707
    new_add = p_add(xor_val, xor_val)
    new_add = p_add(xor_val, new_add)
    new_add = p_add(val, new_add)
    print(hex(new_add))

    return new_add 
    
def main():
    f = open('./' + 'D' * 0x10 + 'C' * 0x10 + 'A' * 0x4f, 'wb') # okay, this does affect how much data is written but why

def find_positions(len_val):
    '''
    a651331b  <-- the last few characters we cannot forget
    0x00007f00a651331b      0x00000000000002c0 <-- maybe there is actually more since we compare for all 16 bytes
    '''
    temp = ['10af39a3030a1613', 'fd74bba036180a0f', '1013483f4b3f1b24', '0a21ddb24e4b0c2e', '00007f00a651331b', '00000000000002c0']
    # temp = ['10af39a3030a1613', 'fd74bba036180a0f', '1013483f4b3f1b24', '0a21ddb24e4b0c2e', '00007f0000000000', '00000000000002c0']
    temp2 = []
    for i in temp:
        temp3 = ''
        for j in range(len(i)-2,-2,-2):
            temp3 += i[j:j+2]
        temp2.append(temp3)
    res = bytes.fromhex(''.join(temp2))
    print(res)

    what_we_want = [0] * (len_val)
    j = 0
    for i in range(len_val):
        print(f"pos {i} goes to pos {j%len_val}")
        if j % len_val < len_val:
            what_we_want[i] = res[j%len_val]
        j+=7
    print(what_we_want)
    return what_we_want

def forward_in_first_branch(user_input, xor_val):
    val = 0x05050505050505050505050505050505 # 16 5's
    user_cp = user_input
    added_val = p_add(val, user_cp)
        
    print(hex(added_val)) # is ok
    xor_val = p_xor(xor_val, added_val)
        # added_val = val + user_input
    # then xor with above value
    print(hex(xor_val))

    val = 0x7070707070707070707070707070707
    new_add = p_add(xor_val, xor_val)
    new_add = p_add(xor_val, new_add)
    new_add = p_add(val, new_add)
    print(hex(new_add))

    return new_add 

def solve2(len_val):
    '''
    Second attempt at solving the problem 
    0x10af39a3030a1613      0xfd74bba036180a0f
    0x1013483f4b3f1b24      0x0a21ddb24e4b0c2e
    a651331b 
    '''
    what_we_want = find_positions(len_val)
    byte_chunks = []
    for i in range(0,len(what_we_want),16):
        print(what_we_want[i:i+16])
        byte_chunks.append(what_we_want[i:i+16])
    print(byte_chunks)
    xor_chunks = [
        '5C5B5A595857565554535251504F4E4D',
        '6C6B6A696867666564636261605F5E5D',
        '7C7B7A797877767574737271706F6E6D', # <-- this value is always used in the second branch i think 
        '8C8B8A898887868584838281807F7E7D',
        '9C9B9A999897969594939291908F8E8D',
        '0ACABAAA9A8A7A6A5A4A3A2A1A09F9E9D',
    ]
    print(len(byte_chunks), len(xor_chunks))
    ret = ''
    for i,v in enumerate(byte_chunks):
        xor_val = xor_chunks[i]
        xor_val = rev_hex(xor_val)
        xor_arr = []
        for j in range(0,len(xor_val),2):
            xor_arr.append(int(xor_val[j:j+2], 16)) 
        print("xor arr: ", xor_arr)
        print("v: ", v)

        # iter_val = v.index(0)
        for j in range(len(v)):
            if v[j] == 0: 
                ret+="A"
                continue
            temp2 = forward(v[j], xor_arr[j])
            print(chr(temp2), hex(temp2))
            ret += chr(temp2)
    print(ret)
    return ret

if __name__ == '__main__':
    candidates = []
    for i in range(0x20, 0x70):
        try:
            val = solve2(i)
            candidates.append(val)
        except:
            break
    for i in candidates:
        print(i)
    
    # Testing
    # forward_in_first_branch(0x41414141414141414141414141414141, 0)
    # forward_in_first_branch(0x44444444444444444444444444444444, 0)


# Flag: DH{6cbfc8649e123d6228133cbad1d0d07f}

