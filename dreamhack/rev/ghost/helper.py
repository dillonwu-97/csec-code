add_vals = [
    0x3345, 0x2b58, 0x0b3f, 0x0807, 0x2dc0, 0x0871, 0x42a2, 0x1f2b,
    0x0871, 0x2cc0, 0x1520, 0x34d5, 0x1c6f, 0x1c80, 0x20fc, 0x3ad1,
    0x2e17, 0x32de, 0x056b, 0x61da, 0x02e2, 0x61f1, 0x24da, 0x0598,
    0x080d, 0x2a9b, 0x501a, 0x3ac3, 0x13e6, 0x5d60, 0x1c6c, 0x4856,
    0x2c87, 0x304d, 0x05d1, 0x61d4, 0x02e2, 0x1ad6, 0x06ca, 0x0d5e,
    0x38cc, 0x4d20, 0x3719, 0x1f42, 0x0522, 0x0200, 0x35e4, 0x3a9f,
    0x0306, 0x0200, 0x0e94, 0x001e, 0x4d9b, 0x524f, 0x18cf, 0x0280,
    0x0f6e, 0x0f6e, 0x3556
]

xor_vals =  [
    0x2b, 0x22, 0x6f, 0x91, 0x6a, 0x57, 0x9a, 0x8b,
    0x57, 0x54, 0xfc, 0x23, 0xd5, 0xe8, 0xb8, 0x43,
    0xb7, 0xec, 0x53, 0x04, 0x0c, 0xf1, 0x0e, 0xb8,
    0xbb, 0xd1, 0xd6, 0xa1, 0xde, 0xfc, 0xf6, 0x4a,
    0x1f, 0x83, 0xb5, 0x1e, 0x0c, 0x04, 0x52, 0xde,
    0xdc, 0x10, 0xbb, 0x9e, 0xee, 0xd4, 0x02, 0x55,
    0x58, 0xd4, 0xb0, 0x08, 0xad, 0x6d, 0xdb, 0x1a,
    0x2a, 0x2a, 0x76
]

def make_payload():
# payload = b'A' + b'\x80' + b'B' * 56 # not sure why but this crashes out?
#
#
# payload = b'\x42' + b'\x41' * 59
    payload = b'\x41\x43\x44\x45\x46' * 12
    # payload = b'\x42\x41' * 30
    # payload = b'\x41\x43' * 30
    # payload = b'\x41' * 60
# assert len(payload) == 60
    f = open('./payload', 'wb')
    f.write(payload)
    f.close()

def get_sbox():
    sbox_data = open('./sbox.bin', 'rb').read() 
    sbox_seg = [sbox_data[i:i+8] for i in range(0,len(sbox_data),8)]
    sbox = []
    for i in sbox_seg:
        temp = int.from_bytes(i,byteorder='little')
        sbox.append(temp)
    return sbox

def sandbox2():
    sbox = get_sbox()
    print(hex(sbox[0x41]), hex(sbox[0x43]), hex(sbox[sbox[0x41]]), hex(sbox[sbox[0x43]]))
    # input()
    arr = [0x41, 0x43] * 30
    sbox_arr = []
    for i in range(len(arr)-1):
        temp = sbox[arr[i]]
        dbl = sbox[temp]
        sin = sbox[arr[i+1]]
        # sbox_arr.append(dbl)
        # sbox_arr.append(sin)

        if dbl < sin:
            sbox_arr.append(dbl)
            sbox_arr.append(sin)
        else: 
            sbox_arr.append(sin)
            sbox_arr.append(dbl)
        # if sin < dbl: 
        # else:
    print(sbox_arr)

    print([hex(i) for i in sbox_arr])
    xor_vals = []
    prev = sbox_arr[0] ^ sbox_arr[1] ^ 0x1
    xor_vals.append(prev)
    for i in range(2,len(sbox_arr)):
        prev = prev ^ sbox_arr[i] 
        xor_vals.append(prev)

    print([hex(i) for i in xor_vals])

def sandbox():
    make_payload()
    sbox = get_sbox()
    arr = [0x41, 0x43] * 30
    print(sbox)
    print(arr)
    sbox_from_arr = []
    for i in arr:
        sbox_from_arr.append(sbox[i])
    print("Sbox from arr")
    print([hex(i) for i in sbox_from_arr])
    print(hex(sbox[55]))

    print(hex(sum(sbox)))
    print(0x5ef + 0x1af7)
    print(hex(sbox[sbox[0x43]]))

def solve():
    make_payload()
    sbox = get_sbox()
    # print(hex(sbox[0x41]), hex(sbox[0x43]), hex(sbox[sbox[0x41]]), hex(sbox[sbox[0x43]]))
    # input()
    arr = [0x41, 0x43] * 30
    # arr = [0x41, 0x43,0x44,0x45,0x46] * 12
    swap_arr = [i for i in range(256)]
    sbox_arr = []

    def do_xor(a, b):
        ret = swap_arr[a]
        for i in range(a+1, b):
            # print(hex(swap_arr[i]))
            ret ^= swap_arr[i]
        return ret
            
               
    # forward algorithm 
    def forward():
        for i  in range(len(arr)):
            x_a = sbox[ arr[i] ] # first deref
            x_b = sbox[ arr[i+1] ]
            y_a = sbox[x_a] # second deref
            y_b = sbox[x_b] 
            s_a = swap_arr[x_b] # swap array 
            s_b = swap_arr[y_a]
            a = s_a
            b = s_b
            temp = None
            if b > a:
                temp = b
                b = a
                a = temp
            sum_val = sum(swap_arr[b:a+1])
            xor_val = do_xor(b, a+1)      # TODO: might have to modify this a little bit, not sure, the current function uses do_xor
            print(chr(arr[i]), chr(arr[i+1]))
            print(hex(b),hex(a))
            print(hex(sum_val))
            print(hex(xor_val))                   
            input('sum, xor looks okay')
            
            # swap 1
            # first iteration looks ok, but swap might be wrong 
            temp = swap_arr[x_b]
            swap_arr[x_b] = swap_arr[y_a]                             
            swap_arr[y_a] = temp 
            print([hex(i) for i in swap_arr])
            input()
    def reverse():
        '''
        forward implementation looks correct, go backwards now
        (43,167) <-- just manually go this value
        a, b values 
        and a, b are derived from the swap array
        '''            # swap 2
     # x_a = sbox[ arr[i] ] # first deref
     #        x_b = sbox[ arr[i+1] ]
     #        y_a = sbox[x_a] # second deref
     #        y_b = sbox[x_b] 
     #        s_a = swap_arr[x_b] # swap array 
     #        s_b = swap_arr[y_a]
     #        a = s_a
     #        b = s_b 
        # i think it could start from reverse as well but we'll see
        a = 43       # swap_arr[43] = 43 at the beginning so 
        b = 167 
        x_b = a # swap_arr equals the value at the beginning so this should be fine
        y_a = b 
        y_b = None
        x_a = None
        for i,v in enumerate(sbox):
            if i == x_b:
                y_b = v
            elif v == y_a:
                x_a = i
        print(x_a, x_b, y_a, y_b)
        print(x_b, y_a)
        input("swaps")
        pos_0 = None
        pos_1 = None
        for i,v in enumerate(sbox):
            if v == x_b:
                pos_1 = i
            elif v == x_a:
                pos_0 = i
        print(pos_0, pos_1)      

    def check_block(correct_xor_val, correct_sum_val, cur_pos, check_val):
        '''
        Check that this block is valid 
        pass in the correct_xor_val, correct_add_val
        this is essentially the stuff inside the for loop 
        '''
        # print(arr)
        # print(arr[cur_pos])
        # input("double checking arr")
        x_a = sbox[ arr[ cur_pos ] ]
        x_b = sbox[ check_val ] # need to find check_val actually
        y_a = sbox[x_a]
        y_b = sbox[x_b]
        s_a = swap_arr[x_b]
        s_b = swap_arr[y_b]
        a = s_a
        b = s_b

        temp = None
        if b > a:
            temp = b
            b = a
            a = temp
        sum_val = sum(swap_arr[b:a+1])
        xor_val = do_xor(b, a+1)     
        print(hex(b),hex(a))
        print(hex(sum_val))
        print(hex(xor_val))                    
        # input()
        ret_val = [None, None, None]
        ret_val[0] = (sum_val == correct_sum_val) and (xor_val == correct_xor_val)
        ret_val[1] = x_b
        ret_val[2] = y_a
        return ret_val
        
    arr = [68, 72]
    def get_original():
        '''
        Get the original input 
        '''

        # need to break this apart 
        # add some check 
        # we already know 0 and 1 values
        # print(sbox[43], sbox[167])

        temp = swap_arr[43]
        swap_arr[43] = swap_arr[167]                             
        swap_arr[167] = temp  
        input()
        for i in range(len(add_vals)):
            flag = False
            x_b = None 
            y_a = None
            for j in range(256):
                ret = check_block(add_vals[i], xor_vals[i], i+1, j)
                ok = ret[0]
                x_b = ret[1]
                y_a = ret[2]
                
                if ok:
                    arr.append(j)
                    flag = True
                    break
            if flag == False:
                input("Failed! something went awry")
            else: 
                print([chr(i) for i in arr])
                input("yay chr is:", chr(arr[-1] ))
                
                # correct_xor_val, correct_sum_val, cur_pos, check_val): 
                # swap 1
                # first iteration looks ok, but swap might be wrong 
                
            temp = swap_arr[x_b]
            swap_arr[x_b] = swap_arr[y_a]                             
            swap_arr[y_a] = temp 
            print([hex(i) for i in swap_arr])
            input() 
            
    forward()
    # reverse()
    # get_original()

def main():
    # sandbox()
    solve()

if __name__ == '__main__':
    main()




