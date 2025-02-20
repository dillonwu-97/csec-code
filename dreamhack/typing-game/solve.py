from pwn import *
def get_words():
    f = open('./dictionary.txt', 'r').read().split('\n')
    return f

dic = get_words()
def hibyte(a):
    return (a >> 8) & 0xff

def get_next(arr, pos):
    a = int.from_bytes(arr[pos], byteorder='big')
    assert len(arr[pos]) == 2
    lo_nibble_a = a & 0xf
    hi_nibble_a = (a >> 4) & 0xf
    lo_nibble_z = (a >> 8) & 0xf
    hi_nibble_z = (a >> 12)
    vals = [lo_nibble_a, hi_nibble_a, lo_nibble_z, hi_nibble_z]
    w = vals[0]
    x = vals[1]
    y = vals[2]
    z = vals[3]

    part1 = (3 * w + 5 * x + 7 * y + 2 * z) % 16
    part2 = (4 * w + 7 * x + 6 * y + 3 * z) % 16
    part3 = (2 * w + 3 * x + 5 * y + 4 * z) % 16
    part4 = (5 * w + 6 * x + 4 * y + 7 * z) % 16

    ret = part1 | (part2 << 4) | (part3 << 8) | (part4 << 12)
    return ret
    

def get_rand(arr):
    for i in range(0,8):
        val1 = int.from_bytes(arr[i], byteorder='big') & 0x8000
        temp = int.from_bytes(arr[(i+1) % 8], byteorder='big') 
        val2 = temp & 0x7fff
        val1 |= val2
        val1 >>= 1
        if (temp & 1) != 0:
            val1 ^= 0x9908 
        val3 = val1 ^ int.from_bytes(arr[(i+4) % 8], byteorder='big')
        arr[i] = val3.to_bytes(2,byteorder='big')
    return arr

def setup_arr(iv): # 4 byte iv value which gets cut into 2 byte chunk 
    # TODO: actually, not sure if this should be little or big endian, need to double check 
    arr = [iv]
    for i in range(1, 8):
        val = int.from_bytes(arr[i-1], byteorder='big')
        val2 = val ^ (val >> 14)
        val2 *= 27655
        val2 += i
        val3 = val2.to_bytes(10, byteorder='big')[-2:]
        arr.append(val3)
    return arr  

    
# 34570 -> 17030
to_save = {}
def build_start():
    ret = {}
    for i in range(0, 1<<16):
        a = setup_arr(i.to_bytes(2, byteorder='big'))
        a = get_rand(a)
        # temp = [int.from_bytes(i, byteorder='big') for i in a]
        b = [get_next(a, i) for i in range(len(a))] # get the positions 
        # c = [dic[i] for i in b]
        # if (b[0] == 6144):
        #     print(i)
        #     input()
        ret[dic[b[0]]] = b
        to_save[dic[b[0]]] = a
    return ret

def get_values(arr): # enter the correct array and get all the values we need
    b = get_rand(arr)
    c = [get_next(b, i) for i in range(len(b))]
    d = get_rand(arr)
    e = [get_next(d, i) for i in range(len(d))]
    ret = [dic[i] for i in c]
    ret += [dic[i] for i in e]
    return ret

def main():

    oto = build_start() # build 1 to 1 mapping
    # print(oto)

    # a1 = setup_arr(b'\xd6\xb8')
    # print([i.hex() for i in a1])
    # print([int.from_bytes(i, byteorder='big') for i in a1])
    # a2 = get_rand(a1)
    # a3 = [get_next(a2, i) for i in range(len(a2))]
    # a4 = get_values(a3)
    # print(a4)
    # print([int.from_bytes(i, byteorder='big') for i in a2])
    # print([i.hex() for i in a2])
    # input()
    # b = get_next(a1, 0)
    # print(b)

    count = 0
    # r = process('./chall')
    r = remote('host1.dreamhack.games', 17259)
    l = r.recvuntil("> ")
    to_send = l.decode().split(": ")[1].split('\n')[0]
    print(f"0: {to_send}")
    values = oto[to_send]
    all_vals = [dic[i] for i in values] + get_values(to_save[to_send])
    print(all_vals)
    l = r.sendline(all_vals[0])
    #
    for i in range(1,20):
        l = r.recvuntil("> ")
        print(f"{i}: {l}")
        # l.decode().split(": ")[1].split('\n')[0]
        r.sendline(all_vals[i])
    r.interactive()


if __name__ == '__main__':
    main()
    # flag: DH{R3C0V3R4BL3_M3RS3NN3_V4R14N7:Pay3Gam1LEyMNIJaS8xfbg==}


