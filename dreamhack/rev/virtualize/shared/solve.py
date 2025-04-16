from pwn import *

'''
trying to send 0x20 bytes in and break at memcmp
maybe i can just brute force the problem
1. start program
2. 
'''

def test():
    r = process('./main_patched')
    io = gdb.debug(["./main_patched"], gdbscript='''
''', api=True)
    io.gdb.Breakpoint('*0x402472') 
    time.sleep(2)
    # io.gdb.continue_and_wait()
    payload = b'\x41' + b'\x00' * 31
    r.sendlineafter("Input: ", payload)
    r.interactive()
    # log.info(r.recvall())

def collect_data(r, payload):
    pid, io_gdb = gdb.attach(r, gdbscript='''
b *0x402472    
c
x/20gx 0x407120
''', api=True)
    print(f"pid: {pid}")
    time.sleep(1)
    r.sendlineafter("Input: ", payload)
    output = io_gdb.execute('x/20gx 0x407120', to_string=True)
    print(output)
    time.sleep(1)
    io_gdb.execute("detach")
    r.close()
    try:
        io_gdb.post_event(io_gdb.execute("quit"))
    except:
        pass
    return output

def data_to_file(filename):
    outputs = []
    for i in range(33):
        r = process("./main_patched")
        if i == 32:
            payload = b'\x41' * 64 # true output
            # payload = b'\x41\x42' * 16 # true output
        else:
            payload = b'\x41' * i + b'\x42' + b'\x41' * (63 - i)
            print(payload)

            print(len(payload))
            # assert len(payload) == 32
        # try:
        output = collect_data(r, payload)
        # except:
        #     continue
        print("output: " , output)
        outputs.append(output)
    to_write = '\n\r'.join(outputs)
    f = open(filename, 'w')
    f.write(to_write)
    f.close()

def track_differences(arr):
    blocks = []
    for i in arr:
        block = ''  
        vals = i.split('\n')
        # print(len(vals))
        vals = [i for i in vals if i != '']
        for (w,j) in enumerate(vals):
            # print(w,j,vals)
            if w == 4: break
            temp = j.split(":")[1]
            temp2 = temp.split("0x")
            s = ''.join(temp2).strip('\t').replace('\t','')
            # print(s)
            block += s
        blocks.append(block)
        # print(len(block), block)
        assert len(block) == 32 * 4
    # print(blocks)
    assert blocks[0] != blocks[-1]
    base_block = blocks[-1]
    diffs = []
    for i,v in enumerate(blocks):
        if i == 32: break
        diff = []
        for j in range(0, len(v), 2):
            if v[j:j+2] != base_block[j:j+2]:
                diff.append(j)
        # print(diff)
        assert len(diff) == 1
        diffs.append(diff[0])

    print(len(diffs), diffs)
    diffs = sorted(diffs)
    print(diffs)


class StateMachine():
    def __init__(self, inp, pos = 0, state = b''):
        self.state = list(state) + [0] * 8
        self.pos = pos
        self.my_buf = [0] * 256 
        self.malloc_ptr = None
        self.inp = inp

        # hook to keep track of changes to values
        self.saved_buf = []
        self.prev_val = 0x0
        self.track_pos = 0
        self.true_positions = [] # the true positions we need to draw from
        self.my_positions = [] # these are the positions we're grabbing from that are currently incorrect

        self.track_state = 0x73f
        self.prev_state = 0x0
    def print_state(self):
        print(f"pos: {self.pos}")
        print(f"val: {self.val}")
    def good_print(self):
        for i in range(0,len(self.my_buf),16):
            temp = self.my_buf[i:i+8]
            temp2 = self.my_buf[i+8:i+16]
            fn = lambda temp: ''.join([hex(j)[2:].zfill(2) for j in temp[::-1]])
            print(f"{fn(temp)} {fn(temp2)}")

    def unscramble(self):
        if self.pos == 0x66a:
            self.good_print()
            self.saved_buf = self.my_buf
            a = self.my_buf[0:64]
            b = self.my_buf[64:128]
            # print(a)
            # input()
            # build mapping
            d = {}
            for i,v in enumerate(a):
                print(hex(v), b.index(v))
                # d[i] = b.index(v)
                d[b.index(v)] = i
            print(d)
            input()

            
    def find_next(self):
        # self.pos %= len(self.state)
        temp = self.state[self.pos] >> 4 
        if self.my_buf[self.track_pos] != self.prev_val:
            self.good_print()
            input(f"Found a change!\n new: {hex(self.my_buf[self.track_pos])}\n prev: {hex(self.prev_val)}")
            self.prev_val = self.my_buf[self.track_pos] 
        if self.state[self.track_state] != self.prev_state:
            input(f"Found a change!\n new: {hex(self.my_buf[self.track_pos])}\n prev: {hex(self.prev_val)}")
            self.prev_state = self.state[self.track_state]

        # self.unscramble()
        # add the hook here 
        if temp == 0:
            self.c0()
        elif temp == 1:
            self.c1_2_3(1)
        elif temp == 3:
            self.c1_2_3(3)
        elif temp == 4:
            self.c4_5(4)
        elif temp == 5:
            self.c4_5(5)
        elif temp == 6:
            self.c6()
        elif temp == 7:
            input("Now entering c7")
            self.c7()
        elif temp == 9:
            # TODO: make this accept user specified input as a byte array
            # self.read(b'\x00' * 64)
            # self.read(b'A' * 64)
            self.read(self.inp)
        elif temp == 10:
            self.write()
        elif temp == 11:
            self.c11()
        else:
            input(f"Something went wrong: {temp} {hex(self.pos)}")
        return temp 

    def c0(self):
        if self.pos in [47, 57, 67, 77, 87, 97, 107]:
            self.good_print()
            input()
        prev = None
        flag = (self.state[self.pos] & 8 != 0)
        print(f"state: 0, flag: {int(flag)}, {self.pos}, {hex(self.pos)}")
        ctr = (self.state[self.pos] & 7) + 1
        self.pos += 1
        offset = self.state[self.pos]
        self.pos += 1

        if flag: # not sure what this flag is but ok
            # I think the flag is used to signal where things are being written
            # yea, all the writes happen when the flag is 1, immediately after malloc
            for i in range(ctr):
                # true positions
                if self.pos < 0x66d and self.pos >= 0x25:
                    self.good_print()
                    print(self.state[self.pos])
                    self.true_positions.append(self.pos)
                    input()

                # input positions
                if self.pos >= 0x66d:
                    # oh yea self.my_buf
                    self.good_print()
                    print(hex(self.pos), hex(self.state[self.pos]))
                    input()
                # self.pos %= len(self.state)
                assert (self.pos < len(self.state)), f"{self.pos}, {len(self.state)}"
                assert (offset + i < len(self.my_buf)), f"{offset + i}, {len(self.my_buf)}"
                self.my_buf[i + offset] = self.state[self.pos]
                self.pos += 1
        else:
            val = self.state[self.pos]
            self.pos += 1
            for i in range(ctr):
                self.my_buf[i + offset] = self.my_buf[i + val]

    def c1_2_3(self, opt): 
        flag = (self.state[self.pos] & 8 != 0)
        count = (self.state[self.pos] & 7) + 1
        self.pos += 1 
        local_pos = self.state[self.pos]
        self.pos += 1 
        if flag:
            # THIS BRANCH IS NEVER ENTERED
            input("FIRST")
            a = 0
            b = 0
            for i in range(count):
                shift = (8 * i)
                a |= (self.my_buf[local_pos + i] << shift)
                b |= (self.state[self.pos] << shift)
                self.pos+=1
            if opt == 1:
                c = a + b
            elif opt == 3:
                c = a ^ b
            for i in range(count):
                self.my_buf[local_pos + i] = (c & 0xff)
                c >>= 8
        else:
            # input("SECOND")
            a = self.state[self.pos]
            self.pos += 1
            b = 0
            c = 0
            for i in range(count):
                shift = (8 * i) 
                c |= (self.my_buf[local_pos + i] << shift)
                b |= (self.my_buf[a + i] << shift)
            if opt == 1:
                d = c + b
            elif opt == 3:
                d = c ^ b
            for i in range(count):
                self.my_buf[local_pos + i] = ( d & 0xff )
                
                d >>= 8

    def c4_5(self, opt):
        flag = (self.state[self.pos] & 8 != 0)
        count = (self.state[self.pos] & 7) + 1
        self.pos += 1 
        local_pos = self.state[self.pos]
        self.pos += 1 
        if flag:
            a = 0
            for i in range(count):
                shift = 8 * i
                a |= ( self.my_buf[local_pos + i] << shift)
            b = self.state[self.pos]
            self.pos += 1
            if opt == 5:
                c = a >> (b % (8 * count)) # some new val to use?
            else: # opt == 4:
                c = a << (b % (8 * count))
            for i in range(count):
                self.my_buf[ local_pos + i ] = ( c & 0xff ) # only the lower byte
                c >>= 8
        else:
            offset = self.state[self.pos]
            self.pos += 1
            a = 0
            for i in range(count):
                shift = 8 * i
                a |= (self.my_buf[local_pos + i] << shift)
            if opt == 5:
                b = a >> (self.my_buf[offset] % (8 * count))
            else: # opt = 4
                b = a << (self.my_buf[offset] % (8 * count))
            for i in range(count):
                self.my_buf[local_pos + i] = ( b & 0xff )
                b >>= 8
    def c6(self): # malloc, ok how emulate this
        print(f"state: 6, {self.pos}, {hex(self.pos)}")
        flag = (self.state[self.pos] & 8 != 0)
        exit_check = (self.state[self.pos] & 7) + 1
        self.pos += 1
        if exit_check != 2:
            input("Error in case 6")
        byte_1 = None
        byte_2 = None
        if flag:
            byte_1 = self.state[self.pos] 
            byte_2 = self.state[self.pos+1]
            self.pos += 2
        else:
            idx = self.state[self.pos]
            self.pos += 1
            byte_1 = self.my_buf[idx]
            byte_2 = self.my_buf[idx + 1]
        # TODO: malloc does some stuff here, but not sure how it's used
        self.malloc_ptr = self.pos & 0xffff
        two_byte_val = (byte_2 << 8) + byte_1
        self.pos = two_byte_val
    def c7(self):
        flag = (self.state[self.pos] & 8 != 0)
        sz = (self.state[self.pos] & 7) + 1
        self.pos += 1
        exit_fn_pos = self.state[self.pos] + (self.state[self.pos+1] << 8)
        self.pos += 2
        if (flag):
            # most likely checking the length
            offset = self.state[self.pos]
            self.pos += 1
            a = 0
            b = 0
            for i in range(sz):
                shift = 8 * i
                a |= self.my_buf[offset + i] << shift
                b |= self.state[self.pos] << shift
                self.pos += 1
            if a == b:
                self.pos = exit_fn_pos
        else:
            pos_a = self.state[self.pos] 
            self.pos += 1
            pos_b = self.state[self.pos]
            self.pos += 1
            for i in range(sz):
                if self.my_buf[pos_a + i] != self.my_buf[pos_b + i]:
                    pos = exit_fn_pos
                    break

    def write(self):
        print("state: 10")
        self.pos+=1
        offset = self.state[self.pos]
        self.pos+=1
        amnt = self.state[self.pos]
        self.pos += 1
        s = ''.join([chr(i) for i in self.my_buf[offset:amnt]])
        print("Write: ", s)

    def read(self, to_read):
        print("state: 9")
        self.pos += 1
        offset = self.state[self.pos]
        self.pos += 1
        amnt = self.state[self.pos]
        # print(f"amnt: {amnt}")
        self.pos += 1
        for i in range(amnt):
            try:
                self.my_buf[offset + i] = to_read[i]
            except:
                break
    def c11(self):
        self.pos += 1
        self.pos = self.malloc_ptr
        self.malloc_ptr = None

def simulate_machine(payload):
    f = open('./bytearray', 'rb').read()
    sm = StateMachine(payload, pos = 0, state=f)
    sm.c0() # startup
    while (1):
        sm.find_next()


def sandbox():
    filename = './collected_data'
    # data_to_file(filename)
    f = open('./collected_data', 'r').read().split('\n\n')
    # f2 = open('./collected_data_2', 'r').read().split('\n\n')
    # f3 = open('./collected_data_3', 'r').read().split('\n\n')
    # print(len(f))
    assert len(f) == 33
    track_differences(f)

    r = process('./main_patched')
    a = 8
    b = 64 - a
    # payload = b'Z' * a + b'B' * b
    # payload = b'A' * a + b'B' * b
    payload = b'Ab3457b487bd91{9aDA6b05bac5B7aa7A}CF2FdafBa1caH2Ba131aDE2ad0e4ac'
    # payload = b''
    # for i in range(32):
    #     payload += b'AB'
    collect_data(r, payload)
    # track_differences(f2)
    # brute force each of the positions?
    # for each of those, find the correct value afterwards?
    # for i in f:
    #     print(i)
    #     input()
    
def solve():
    key_chunks = ['08493e3e6f22cfe2', '4eb4affd83ef5c5c']
    flag_chunks = [
        "4b6f4d6d2c11e9f6",
        "dd03bc6ec5c92fdf",
        "2e1a3d180c368bf4",
        "3da2b98ea7bc6a4a",
        "1e0f5a1d0b1618f6",
        "6d30b9cb90f9783a",
        "5c0d282d5c31d9c6",
        "78a2ecab80a94a7f"
    ]

    key = b''
    flag = b''
    rev_fn = lambda v: [v[i:i+2] for i in range(len(v)-2, -1, -2)]

    for v in key_chunks:
        temp =  rev_fn(v)
        for j in temp:
            key += bytes.fromhex(j)
    for v in flag_chunks:
        temp = rev_fn(v)
        for j in temp:
            flag += bytes.fromhex(j)
    print(key.hex())
    print(flag.hex())
    ret = b''
    for i,v in enumerate(flag):
        temp = flag[i] ^ key[i % len(key)]
        a = (temp & 0xf) << 4
        b = temp >> 4
        c = a + b
        print(hex(temp), hex(c))
        ret += int.to_bytes(c, byteorder='little', length=1)
    print(ret)
    d = {17: 0, 46: 1, 14: 2, 37: 3, 26: 4, 16: 5, 45: 6, 39: 7, 9: 8, 6: 9, 59: 10, 2: 11, 34: 12, 61: 13, 25: 14, 35: 15,63: 16, 56: 17, 40: 18, 21: 19, 28: 20, 23: 21, 44: 22, 19: 23, 30: 24, 52: 25, 18: 26, 60: 27, 47: 28, 11: 29, 54: 30, 36: 31, 4: 32, 12: 33, 8: 34, 32: 35, 49: 36, 51: 37, 27: 38, 31: 39, 50: 40, 0: 41, 29: 42, 10: 43, 1: 44, 43: 45, 38: 46, 55: 47, 58: 48, 7: 49, 57: 50, 3: 51, 62: 52, 5: 53, 53: 54, 24: 55, 20: 56, 41: 57, 22: 58, 13: 59,15: 60, 42: 61, 48: 62, 33: 63}
    ret2 = [0] * len(ret)
    for i,v in enumerate(d.keys()):
        ret2[ d[v] ] = ret[ v ]
    ret2 = b''.join([int.to_bytes(i, byteorder='little', length=1) for i in ret2])
    print(ret2)

def main():
    # simulate_machine(b'Ab3457b487bd91{9aDA6b05bac5B7aa7A}CF2FdafBa1caH2Ba131aDE2ad0e4ac')
    # simulate_machine(b'Bcd3Aa7aC81a}03e7A5b26d0E{5dbaaaFc9974H4Aa4a5bb7a2fFcDa2D1BbB11a')
    # payload = b''
    # for i in range(1,65):
    #     payload += int.to_bytes(i, byteorder='little', length=1)
    # simulate_machine(payload)

    solve()

if __name__ == '__main__':
    main()
    
