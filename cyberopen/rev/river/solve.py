def child_1(inp_arr):
    c1_arr = [ 0xbb, 0x55, 0x62, 0xac, 0xfc, 0x5f, 0x80, 0x5b, 0xb3, 0xc0, 0xea, 0xd7, 0xa8, 0x85, 10, 0x5a, 0xf8, 0x66, 0x59, 0xaa, 0xc2, 0x93, 0x91, 0x28, 0xff, 0x78, 0x9c, 0x8a, 0x66, 0xa4, 0x44, 0x3a, 0x73, 0xf7, 0x8f, 8, 0xfa, 0x75, 0xba]

    # for i in range(0, 0x27):
    #     c1_arr[i] ^= inp_arr[i]
    # return c1_arr

    for i in range(0, 0x27):
        inp_arr[i] ^= c1_arr[i]
    return inp_arr

def child_2(in_arr):
    for i in range(0, 0x27):
        in_arr[i] ^= 0x56
    return in_arr

def child_3(in_arr):

    # Forward
    # var_ed = 0
    # for i in range(0, 0x27):
    #     in_arr[i] ^= var_ed
    #     var_ed = in_arr[i]
    # return in_arr

    # Backward
    for i in range(0x26, 0, -1):
        in_arr[i] ^= in_arr[i-1]
    in_arr[0] ^= 0
    return in_arr

def translate(arr):
    # print(arr)
    print(''.join([chr(i) for i in arr]))

def final_result():
    inp_arr = [ 0x99, 0x69, 0x3b, 0xfc, 0x9d, 0x1a, 0xa0, 0x19, 0xd3, 0xa9, 0x87, 0xdd, 0x82, 0xca, 0x61, 0x38, 0xff, 0x55, 0x5e, 0xce, 0xaf, 0x9c, 0xa6, 0xd, 0xd3, 100, 0x9a, 0xea, 0x27, 0x86, 0x6f, 0x7f, 1, 0xe0, 0xad, 0x48, 0xdd, 0x61, 0x9a]
    # Going backwards, it's xor with array, xor with previous vals, xor with 0x56
    
    step1 = child_1(inp_arr)
    step2 = child_3(step1)
    step3 = child_2(step2)
    print(step3)
    print(translate(step3))
    # tH3_gr34t_R1v3r_3bb5_4nD_fL0w5_8a3c41eb



    
    # translate(child_1(child_2(child_3(inp_arr))))
    # translate(child_1(child_3(child_2(inp_arr))))
    # translate(child_2(child_1(child_3(inp_arr))))
    # translate(child_2(child_3(child_1(inp_arr))))
    # translate(child_3(child_1(child_2(inp_arr))))
    # translate(child_3(child_2(child_1(inp_arr))))

    # translate(child_3(inp_arr))
    # translate(child_2(inp_arr))
    # translate(child_1(inp_arr))
    

def main():
    final_result()

if __name__ == '__main__':
    main()