# 0x7fffffffe230: 0x1f6d5e4391523728      0x612270554694793a
# 0x7fffffffe240: 0x73644967583d8b7c      0x00765b4c6a4f408e
#
def rev_hex(s):
    ret = [s[i:i+2] for i in range(len(s)-2,-2,-2)]
    return ''.join(ret)

def construct_map():
    '''
    Build out injection map 
    user input pos
    stack output pos 
    '''
    # 0x7fffffffe2a0: 0x3d46434c49221f28      0x555e5b64613a3740
    # 0x7fffffffe2b0: 0x6d76737c79524f58      0x008e8b94916a6770
    #
    # output_vals = []
    # 0x1f6d5e4391523728      0x612270554694793a
    # 0x73644967583d8b7c      0x00765b4c6a4f408e
    #
    # input_str = '281f22494c43463d40373a61645b5e55584f52797c73766d70676a91948b8e00' # intermediate value
    # output_str = '28375291435e6d1f3a799446557022617c8b3d58674964738e404f6a4c5b7600' # output value
    #
    # input_str = '281f22494c43463d40373a61645b5e55584f52797c73766d70676a91948b8e85'
    # output_str = '286d5e4394793a1f7055468b7c612267583d8e7364496a4f4085765b4c915237'

    # output_str = '13160a0303a39af10fa01836a0bb74fd24b1f3b4f38d34102ec0b4e2b2dd21a0' <-- gpt generated garbage
    # output_str = '13160a03a339af100f0a1836a0bb74fd241b3f4b3f4813102e0c4b4eb2dd210a'
    # input_str = '131074b2483b181b0a0ae0f3bbfa0a2e2401219a34bb4b160fd13dd3a6363f0c'
    
    output_str = ['1f3a7994435e6d28','6722617c8b465570','4f6a4964738e3d58','3752914c5b768540']
    output_str = ''.join([rev_hex(i) for i in output_str])

    input_str = ['3d46434c49221f28','555e5b64613a3740','6d76737c79524f58','858e8b94916a6770']
    input_str = ''.join([rev_hex(i) for i in input_str])


    # input_stuff = ['1b1803b248740113', '2e0aafbb3f4e0a0a','164b4ba039211024','0c3f36a3dd13fd0f']
    # input_str = ''.join([rev_hex(i) for i in input_stuff])
    print(input_str)

    input_arr = [input_str[i:i+2] for i in range(0,len(input_str),2)]
    output_arr = [output_str[i:i+2] for i in range(0,len(output_str),2)]

    print(input_arr) # scrambled indices, return
    print(output_arr) # 0 -> n
    input()
    # there is redundancy but idc
    temp = []
    for i,v in enumerate(input_arr):
        temp.append(output_arr.index(v))
    print(temp)
    return temp
    # ret = [0] * 32
    # for i,v in enumerate(temp):
    #     ret[v] = i 
    # print(ret)
    # input()
    # return ret

def construct_inter(pos, to_rearrange):
# 0x7fffffffe200: 0x13160a03a339af10      0x0f0a1836a0bb74fd <-- big endian representation from little
# 0x7fffffffe210: 0x241b3f4b3f481310      0x2e0c4b4eb2dd210a
    # inter_str = '13160a03a339af100f0a1836a0bb74fd241b3f4b3f4813102e0c4b4eb2dd210a'
    # inter_str = '281f22494c43463d40373a61645b5e55584f52797c73766d70676a91948b8e00' # test str
    inter_str = to_rearrange
    inter_arr = [inter_str[i:i+2] for i in range(0,len(inter_str),2)]
    ret = []
    for i in pos:
        ret.append(inter_arr[i])
    print(ret)
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
    

def get_16(s, xor_arr, what_we_want):
    '''
    Reverse first 16 bytes
    '''
    arr_a = [int(s[i:i+2],16) for i in range(0,len(s),2)]
    print("arr a: ", arr_a)
    arr_b = []
    for i,v in enumerate(arr_a):
        print(v)
        temp2 = forward(v, xor_arr[i])
        if temp2 == -1:
            input("Not found")
        arr_b.append(temp2)
    print("arr b: ", arr_b)
    print([chr(i) for i in arr_b])
    return arr_b

def main():
    scramble_arr = construct_map()
    print(scramble_arr)
    interm_val = construct_inter(scramble_arr, '286d5e4394793a1f7055468b7c612267583d8e7364496a4f4085765b4c915237')
    print(interm_val)
    assert '281f22494c43463d40373a61645b5e55584f52797c73766d70676a91948b8e85' == interm_val

    print(interm_val, len(interm_val))

    # original
    # inter_str = '13160a03a339af100f0a1836a0bb74fd241b3f4b3f4813102e0c4b4eb2dd210a'
    # inter_str = '13160a03a339af100f0a1836a0bb74fd241b3f4b3f4813102e0c4b4eb2dd210a'
    # inter_str = '28823452b8821c22882264b288221c825852c4822852ac5258b2942258b24c52'
    temp = ['10af39a3030a1613', 'fd74bba036180a0f', '1013483f4b3f1b24', '0a21ddb24e4b0c2e']
    what_we_want = ''.join([rev_hex(i) for i in temp])

    interm_val = construct_inter(scramble_arr, what_we_want)
    assert len(interm_val) == 64
    print(f"intermediate value: {interm_val}")
    input("Got the intermediate value we need to solve for")
    # rearranged
    # 130a3f4e39741016184bb2affd2e0a363fdd10240c03a048210f1b4ba3bb130a 64
    #
    # enc_val = '281f22494c43463d40373a61645b5e55'
    # first_16(enc_val)
    
    # enc_val = '584f52797c73766d70676a91948b8e00'
    # sec_16(enc_val)

    print("Solving")
    xor_arr_first = [92, 91, 90, 89, 88, 87, 86, 85, 84, 83, 82, 81, 80, 79, 78, 77][::-1]
    xor_arr_second = [i for i in range(0x5d, 0x6c+1)]
    first_16 = get_16(interm_val[:32], xor_arr_first, what_we_want[:32])
    print(''.join([chr(i) for i in first_16]))
    second_16 = get_16(interm_val[32:], xor_arr_second, what_we_want[32:])
    arr = first_16 + second_16
    byte_val = b''.join([int.to_bytes(i, byteorder='little') for i in arr])
    print(byte_val.hex())
    byte_val = b'Z' * 32
    f = open('./' + 'D' * 0x10 + 'C' * 0x10 + 'A' * 0x4f, 'wb') # okay, this does affect how much data is written but why
    # because there is a filename_len plus xor pos
    #
    f.write(byte_val)

def find_positions(len_val):
    '''
    
    '''
    temp = ['10af39a3030a1613', 'fd74bba036180a0f', '1013483f4b3f1b24', '0a21ddb24e4b0c2e']
    temp2 = []
    for i in temp:
        temp3 = ''
        for j in range(len(i)-2,-2,-2):
            temp3 += i[j:j+2]
        temp2.append(temp3)
    res = bytes.fromhex(''.join(temp2))
    print(res)

    what_we_want = [0] * len_val
    j = 0
    for i in range(len_val):
        print(f"pos {i} goes to pos {j%len_val}")
        if j % len_val < 0x20:
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

def solve2():
    '''
    Second attempt at solving the problem 
    0x10af39a3030a1613      0xfd74bba036180a0f
    0x1013483f4b3f1b24      0x0a21ddb24e4b0c2e
    '''
    what_we_want = find_positions(0x23)
    byte_chunks = []
    for i in range(0,len(what_we_want),16):
        print(what_we_want[i:i+16])
        byte_chunks.append(what_we_want[i:i+16])
    print(byte_chunks)
    xor_chunks = [
        '5C5B5A595857565554535251504F4E4D',
        '6C6B6A696867666564636261605F5E5D',
        '7C7B7A797877767574737271706F6E6D',
        '8C8B8A898887868584838281807F7E7D',
        '9C9B9A999897969594939291908F8E8D',
        '0ACABAAA9A8A7A6A5A4A3A2A1A09F9E9D',
    ]
    print(len(byte_chunks), len(xor_chunks))
    for i,v in enumerate(byte_chunks):
        xor_val = xor_chunks[i]
        xor_val = rev_hex(xor_val)
        xor_arr = []
        for j in range(0,len(xor_val),2):
            xor_arr.append(int(xor_val[j:j+2], 16)) 
        print(xor_arr)
        print(v)

        # iter_val = v.index(0)
        for j in range(len(v)):
            if v[j] == 0: continue
            temp2 = forward(v[j], xor_arr[j])
            print(chr(temp2), hex(temp2))

if __name__ == '__main__':

    # for i in range(256):
    #     temp = (i + 5) % 256
    #     temp ^= 82
    #     temp = (temp * 3) % 256
    #     temp = (temp + 7) % 256
    #     if temp == 0x3:
    #         input(i)
    # input()
    # main()
    solve2()

    
    # Testing
    # forward_in_first_branch(0x41414141414141414141414141414141, 0)
    # forward_in_first_branch(0x44444444444444444444444444444444, 0)



