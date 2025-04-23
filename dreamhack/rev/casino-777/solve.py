from pwn import *
from time import *
from sympy.ntheory.modular import crt


r = process('./casino_777')
r = remote('host3.dreamhack.games', 21649)
def rotate(ctr):
    r.sendlineafter("> ", "2")
    r.sendlineafter("> ", str(ctr))
    l = r.recvline().decode()
    # print(l)
    vals = l.split("Result: ")[1].split(" ")[:-1]
    return vals

def get_real_pos(pos):
    a = [0x48, 0x52,0x58,0x60,0x66,0x4e,0x64,0x7e,0x82,0x88]
    a = [i+1 for i in a]
    real_pos = [a[i] - pos[i] for i in range(len(pos))]
    return real_pos

def main():
    r.sendlineafter("> ", "1")
    flag = 0
    pos = [-1] * 10
    front_diff = []
    ctr = 1
    gdb_flag = 0
    all_chars = [[] for i in range(10)]
    
    # store all characters seen in a 2d array because this might actually be easier
    slots = rotate(0)
    cmp_save = slots
    for i,v in enumerate(slots):
        all_chars[i].append(v)

    while flag != 10:
        # print(ctr, flag)
        # print(pos)
        slots = rotate(1)
        for i,v in enumerate(slots):
            all_chars[i].append(v)
        if '7' in slots:
            # print("slots: ", slots)
            for i,v in enumerate(slots):
                if pos[i] == -1 and v == '7':
                    pos[i] = ctr
                    flag += 1
                    # print("pos: ", pos)
        ctr += 1
        
    sev_pos = [-1] * 10
    for i in range(10):
        for j,v in enumerate(all_chars[i]):
            if v == '7':
                sev_pos[i] = j
    # print("sev pos: ", sev_pos)
    print([all_chars[i][ sev_pos[i] ] for i in range(10)])
    a = [0x48,0x52,0x58,0x60,0x66,0x4e,0x64,0x7e,0x82,0x88] # n values
    a = [i+1 for i in a]
    z = [0] * 10
    zero_crt = crt(a, z)[1] # number of rotations to reset
    print(f"zero crt: {zero_crt}")

    # subtract by number we have already rotated
    # print(all_chars[0][0x49], all_chars[0][0x0])
    # print(all_chars[0])
    # zero_crt = 0x49 * 1000000000070000000
    # zero_crt = 97981473640378183091
    # zero_crt = 1342211967676413467 * 0x49
    max_send = (1<<63)-1
    for i in range(zero_crt // max_send):
        slots = rotate(max_send)
        zero_crt -= max_send
    zero_diff = zero_crt - ctr
    assert zero_diff < max_send
    print(f"zero diff: {zero_diff}, {ctr}")
    slots = rotate(zero_diff)
    slots = rotate(1)
    print("new: ", slots)
    print(all_chars[0].index(slots[0]))
    print(all_chars[0].index(cmp_save[0]))
    print("original: ", cmp_save)

    print("Done resetting to original positions")
    
    # sev_pos = remainder values
    crt_val = crt(a, sev_pos)[0]
    print(crt_val)
    # input()
    # print(all_chars[1])
            
    for i in range(crt_val // max_send):
        slots = rotate(max_send)
        crt_val -= max_send
    slots = rotate(crt_val)
    print("new: ", slots)

    r.interactive()

if __name__ == '__main__':
    main()
    # flag: DH{01b85f246095797859d9ff9e54aaebf4707f715a}

