
def get_data(fname):
    sbox_data = open(fname, 'rb').read() 
    sbox_seg = [sbox_data[i:i+8] for i in range(0,len(sbox_data),8)]
    sbox = []
    for i in sbox_seg:
        temp = int.from_bytes(i,byteorder='little')
        sbox.append(temp)
    return sbox 

sbox = get_data('./sbox.bin')
def sandbox():
    sbox = get_data('./sbox.bin')
    print("Our current sbox values / currently incorrect")
    print([hex(i) for i in sbox])
    print(hex(sbox[0x41]))
    # input()

    correct = get_data('./correct.bin')
    print("-" * 20)
    print("correct values / values we want")
    print([hex(i) for i in correct])

    init_segment_tree = get_data('./init_seg.bin')
    print("-" * 20)
    print("initial segment tree")
    print([hex(i) for i in init_segment_tree])
    assert len(init_segment_tree) == 256

    swap_arr = [i for i in range(256)]
    assert len(swap_arr) == 256

    new_arr = []
    sz = 48
    payload = [0x41] * sz
    for i in payload:
        new_arr.append(sbox[i])

    print("-" * 20)
    print("new array from swap array: ")
    print([hex(i) for i in new_arr])
    print("-" * 20)

    print(hex(init_segment_tree[0x3f]))
    print(hex(init_segment_tree.index(0x19c)))
    print(hex(init_segment_tree.index(0x278)))
    # the two above sum to 0x414
    print("sbox-----")
    print(hex(sbox[0x43]))
    # print(hex(sbox[sbox[0x43]]))
    print(hex(sbox[0x44]))


def xor(arr):
    ret = 0
    for i in arr:
        ret ^= i
    return ret

def add(arr):
    ret = 0
    for i in arr:
        ret += i
    return ret

def mult(arr):
    ret = 1
    for i in arr:
        ret *= i
    return ret 

def add_range(a, b):
    total = 0
    for i in range(a,b):
        total += i
    return total


def check_nib(a, b, nib, mult):
    return ((mult * add_range(a, b+1)) & 0xF) == nib


def get_tuple_candidates(start, nibbles, mult):
    '''
    nibbles = array of nibbles

    TODO: i can restrict the range to printable ascii instead actually 
    '''
    n_a = nibbles[0]
    n_b = nibbles[1]
    n_c = nibbles[2]
    n_d = nibbles[3]

    c1 = [] # first candidates
    for i in range(0, 256):
        if check_nib(0, i, n_a, mult):
            c1.append(i)

    c2 = [] # second candidates (pairs)
    for v in c1: # for each candidate, this becomes our new start position
        a = None
        b = None
        for i in range(0, 256):
            sbox_check = sbox.index(i) 
            if sbox_check < 32 or sbox_check > 128:
                continue
            a = min(i, v)
            b = max(i, v)
            if check_nib(a, b, n_b, mult):
                c2.append([v, i])

                

    c3 = []
    for v in c2:
        a = None
        b = None
        for i in range(0, 256):
            sbox_check = sbox.index(i) 
            if sbox_check < 32 or sbox_check > 128:
                continue 
            a = min(i, v[-1])
            b = max(i, v[-1])
            temp = v.copy()
            if check_nib(a, b, n_c, mult):
                temp.append(i)
                c3.append(temp)
    print(len(c3))
    c4 = []
    for v in c3:
        a = None
        b = None
        for i in range(0, 256):
            sbox_check = sbox.index(i) 
            if sbox_check < 32 or sbox_check > 128:
                continue  
            a = min(i, v[-1])
            b = max(i, v[-1])
            temp = [0] + v.copy()
            if check_nib(a, b, n_d, mult):
                temp.append(i)
                c4.append(temp) 

    return c4

    
    

def solve():
    sol = [ord('H')]

    sbox = get_data('./sbox.bin')
    print("Our current sbox values / currently incorrect")
    print([hex(i) for i in sbox])
    print(hex(sbox[0x41]))
    # input()

    correct = get_data('./correct.bin')
    print("-" * 20)
    print("correct values / values we want")
    print([hex(i) for i in correct])

    cells = []
    for i in range(0,len(correct),4):
        cells.append(correct[i:i+4])
    print(cells)

    seg_tree = [i for i in range(256)]
    print(len(cells))
    # input()
    for i,v in enumerate(cells):
        if i != 10: continue
        temp = v[3] # nibble store
        a = (temp >> 12) & 0xF
        b = (temp >> 8) & 0xF
        c = (temp >> 4) & 0xF
        d = temp & 0xF
        nibbles = [ a, b, c, d ]
        print([hex(i) for i in v], nibbles)
        c4 = get_tuple_candidates(32, nibbles, i+1)
        for j,w in enumerate(c4):
        # TODO:
        # construct the range values we need for each of them 
        # maybe they should be done by the tuple_candidates function actually 
            # print("w: ", w)
            add_val = v[0]
            xor_val = v[1]
            mul_val = v[2]

            # print("w: ", [hex(i) for i in w])
            temp = []
            for k in range(1,len(w)):
                a = min(w[k-1], w[k])
                b = max(w[k-1], w[k])
                temp2 = add_range(a, b+1)
                temp.append(temp2) 
            temp = [(i+1) * val for val in temp]
            my_xor = xor(temp)
            my_add = add(temp)
            # my_prod = mult(temp)
            # if temp[0] == 0xcf9:
            #     print(temp)
            #     print(hex(my_add), hex(add_val))
            #     input()
            # if i == 1:
                # print(hex(add_val), hex(my_add)) 
            if my_add == add_val and my_xor == xor_val:
                print("w: ", [hex(i) for i in w])
                sol.append(w)
                input("FOUND")
                break
        print(sol)
        # input("failed")

def get_flag(sbox, arr):
    flag = ''
    for i,v in enumerate(arr):
        for k,j in enumerate(v):
            if k == 0: continue
            temp = sbox.index(j)
            print(temp, chr(temp))
            flag += chr(temp)
    print(flag)


def main():

    f = open('./payload', 'wb')
    # payload = b'DH{' + b'A' * 45
    # payload = b'A' * 48
    payload = b'ACDE'
    for i in range(11):
        payload += int.to_bytes(i + 0x43) * 4
    print(payload)
    f.write(payload)
    f.close()

    f = open('./payload2', 'wb')
    # payload = b'DH{' + b'A' * 45
    payload = b'D' * 48
    f.write(payload)
    f.close()
    #
    # sandbox()
    #
    # total = 0
    # for i in range(0x37, 0x95):
    #     total += i
    # print(hex(total)) 
    #
    sbox = get_data('./sbox.bin')
    print(hex(sbox[ord('D')]))
    print(hex(sbox[ord('H')]))
    print(hex(sbox[ord('{')]))
    print(hex(add_range(0x2b, 0x52)))
    total = 0
    for i in range(0x0, 0x52):
        total += i
    print("total: ", hex(total)) 
    # solve() # i think each is off by 1?
    #
    #
    # a = [[0, 81, 43, 174, 43], [0, 183, 102, 102, 226], [0, 142, 42, 180, 226], [0, 71, 64, 223, 42], [0, 227, 183, 89, 193], [0, 227, 64, 183, 227], [0, 241, 241, 199, 227]]
    #
    # a = [[0, 3, 3, 205, 155]]
    # a = [[0, 64, 39, 193, 227], [0, 42, 226, 211, 42], [0, 42, 41, 40, 51]]
    # a = [[0, 35, 182, 121, 180]]
    a = [[0, 28, 183, 94, 142]]

    get_flag(sbox, a)



    # [72, [0, 64, 39, 193, 227]] # <-- starting for pos 8, (7 taking long af time)
    # [72, [0, 64, 39, 193, 227], [0, 42, 226, 211, 42]]

    # [[0, 64, 39, 193, 227], [0, 42, 226, 211, 42], [0, 42, 41, 40, 51]]


if __name__ == '__main__':
    f = open('./payload', 'wb')
    payload = b'DH{H3ll0!_G0hst_r3vers3r~~Or..M4sTer_0f_z3?!_;)}'
    print("length: ", len(payload))
    f.write(payload)
    f.close()
    # main()

    # flag: DH{H3ll0!_G0hst_r3vers3r~~Or..M4sTer_0f__;)}
