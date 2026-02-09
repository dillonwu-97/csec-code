from unicorn import *
from capstone import *
from unicorn.x86_const import *
import numpy as np

def get_assembly(hexdump):
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    
    # 3. Iterate and print instructions
    for insn in md.disasm(hexdump, 0x0):
        print(f"0x{insn.address:x}:    {insn.mnemonic:<10} {insn.op_str}")

def get_chunks():
    # Get the important chunks
    f = open('./main', 'rb').read()
    c = bytes.fromhex('39C20F95C084C00F')
    a = f.split(c)
    temp = a[0].split(b'\x0f\x85\xb6\x90\x02\x00')[1:][0]
    a[0] = temp
    print(a[0].hex())
    # print(len(a))
    # input()
    # print(a[0].hex()[:100])
    # input()
    return a

class Block():
    def __init__(self, esi, mul):
        self.pos = esi # stores position
        self.mul = mul # stores mult value 

class solver():

    def __init__(self, chunk, start_addr = 0x40000): 
        self.md = Cs(CS_ARCH_X86, CS_MODE_64)
        self.mu =Uc (UC_ARCH_X86, UC_MODE_64)
        # MEM_START = 0x400000
        MEM_START = start_addr

        INC = 0x20000 # size we need for the chunks 
        self.start = MEM_START
        self.inc = INC

        try: 
            STACK_START = 0xf0000
            PAYLOAD_OFFSET = 0x50
            self.mu.mem_map((MEM_START // 0x1000) * 0x1000, INC)
            self.mu.mem_map(STACK_START - INC, INC * 2)

            self.mu.mem_write(MEM_START, chunk )
            payload = b'ABCDEFG' * 10
            # payload = b'AAAABBB' * 10
            self.payload = payload
            # payload = b'AAAAAAA' * 10
            # payload = b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
            self.mu.mem_write(STACK_START - 0x10000, payload)
            ptr = int.to_bytes(STACK_START - 0x10000, byteorder='little', length=8)
            self.mu.mem_write(STACK_START-PAYLOAD_OFFSET, ptr) #

            # need to add hook for call operations
            self.mu.hook_add(UC_HOOK_CODE, self.hook_fn, begin=MEM_START, end=MEM_START + INC)
            
            self.mu.reg_write(UC_X86_REG_RBP, STACK_START)      
            self.mu.reg_write(UC_X86_REG_RSP, STACK_START)      
            self.mu.reg_write(UC_X86_REG_RIP, MEM_START)      
            self.mu.reg_write(UC_X86_REG_RAX, 0x0)      
            self.mu.reg_write(UC_X86_REG_RCX, 0x78)      
            # self.mu.reg_write(UC_X86_REG_RSI, 0x4)      
            self.mu.reg_write(UC_X86_REG_R9, 0x7)      
            self.mu.reg_write(UC_X86_REG_R11, 0x46)     
            self.mu.reg_write(UC_X86_REG_R12, 0x1)     
            self.mu.reg_write(UC_X86_REG_R13, 0x0)     
            self.mu.reg_write(UC_X86_REG_R14, 0xC8312BCFABCB5FC8)      
            self.mu.reg_write(UC_X86_REG_R15, 0x370287DEECE3E277)      

            self.ops = []
            self.matrix = []
            self.block_arr = []
            self.final_val = -1
            self.check_me = -1
            self.check_arr = []
            # self.mu.emu_start(MEM_START, MEM_START + INC)

            # self.ops = []
        except Exception as e:
            print("Exception hit")
            print("rbp: ", hex(self.mu.reg_read(UC_X86_REG_RBP)))
            print("rsp: ", hex(self.mu.reg_read(UC_X86_REG_RSP)))
            print("rip: ", hex(self.mu.reg_read(UC_X86_REG_RIP)))
            print(e)

    def hook_fn(self, uc, address, size, user_data):
        # replace call with 
        # print(hex(address), size)
        try:
            code = self.mu.mem_read(address, size)
            for i in self.md.disasm(code, 0x0):
                # give pointer to position
                try: 
                    # print(f"Addr: {hex(address)}", i.mnemonic, i.op_str)
                    self.ops.append(f"{i.mnemonic} {i.op_str}")
                except:
                    # print(f"Addr: {hex(address)}", i.mnemonic)
                    self.ops.append(i.mnemonic)

                if 'call' in i.mnemonic:
                    # offset = int.from_bytes(self.mu.reg_read(UC_X86_REG_RSI), byteorder='little')
                    offset = self.mu.reg_read(UC_X86_REG_RSI)
                    rdi = self.mu.reg_read(UC_X86_REG_RDI)

                    ptr_to_strptr = int.from_bytes(self.mu.mem_read(rdi, 8), byteorder='little')
                    ptr_to_strptr += offset
                    strptr = self.mu.mem_read(ptr_to_strptr, 8)
                    # print(f"offset: {offset} and ptr to str: {hex(ptr_to_strptr)}")
                    # print(f"strptr: {strptr.hex()}")
                    self.mu.reg_write(UC_X86_REG_RDX, 0x0)
                    self.mu.reg_write(UC_X86_REG_RAX, ptr_to_strptr)
                    rip = self.mu.reg_read(UC_X86_REG_RIP)
                    self.mu.reg_write(UC_X86_REG_RIP, rip + size)

                    # print("rax: ", hex(self.mu.reg_read(UC_X86_REG_RAX)))
                    # print("rbx: ", hex(self.mu.reg_read(UC_X86_REG_RBX)))
                    # print("rdx: ", hex(self.mu.reg_read(UC_X86_REG_RDX)))
                    # print("rsi: ", hex(self.mu.reg_read(UC_X86_REG_RSI)))
                    # print("r14: ", hex(self.mu.reg_read(UC_X86_REG_R14)))
                    # print("r15: ", hex(self.mu.reg_read(UC_X86_REG_R15)))

                    # input()
                    
                elif 'cmp' in i.mnemonic:
                    # print("rax: ", hex(self.mu.reg_read(UC_X86_REG_RAX)))
                    # print("rbx: ", hex(self.mu.reg_read(UC_X86_REG_RBX)))
                    # print("rdx: ", hex(self.mu.reg_read(UC_X86_REG_RDX)))
                    # print("rsi: ", hex(self.mu.reg_read(UC_X86_REG_RSI)))
                    # print("r14: ", hex(self.mu.reg_read(UC_X86_REG_R14)))
                    # print("r15: ", hex(self.mu.reg_read(UC_X86_REG_R15)))
                    self.final_val = self.mu.reg_read(UC_X86_REG_RAX)
                    self.check_me = self.mu.reg_read(UC_X86_REG_RDX)
                    self.mu.emu_stop()
                elif 'lea' in i.mnemonic and '[rbp' in i.op_str:
                    print("rax: ", hex(self.mu.reg_read(UC_X86_REG_RAX)))
                    print("rbx: ", hex(self.mu.reg_read(UC_X86_REG_RBX)))
                    self.check_arr.append(self.mu.reg_read(UC_X86_REG_RBX))
                    # input("pause")

                # else:
                    # print("Nothing ")
        except UcError as e:
            print("Error in hook: ", e)

    def run(self):
        self.mu.emu_start(self.start, self.inc+self.start)


    def split_to_blocks(self):
        # Executed after getting the assembly, split the blocks into chunks 
        
       
        blocks = []
        temp = []
        
        # Split on lea eax        
        for i,v in enumerate(self.ops):
            if 'lea rax, ' in v:
                blocks.append(temp)
                temp = []
            else:
                temp.append(v)
        blocks.append(temp)
        blocks = blocks[1:]

        for i,v in enumerate(blocks):
            pos = -1
            mul_val = 0
            # print(v)
            # input()
            for j, v2 in enumerate(v):
                if 'mov esi, ' in v2:
                    temp = v2.split('mov esi, ')[1]
                    if '0x' in temp:
                        temp = temp[2:]
                    temp = int(temp, 16)
                    pos = temp
            for j, v2 in enumerate(v):
                if 'imul' in v2:
                    flag = True
                    x = v2.split('eax, 0x')[1]
                    mul_val = int(x,16)
            if mul_val == 0: # means we have to do it again
                x = 1
                flag2 = False
                y = 1
                for j,v2 in enumerate(v):
                    # print(v2)
                    if 'shl' in v2:
                        flag2 = True
                        aa = v2.split('shl eax, ')[1]
                        if '0x' in aa:
                            aa = aa[2:]
                        aa = int(aa, 16)
                        x *= 2**aa 
                    elif 'add ebx' in v2:
                        break
                    elif 'add eax, edx' in v2:
                        x += y
                    elif 'rax' in v2 and 'lea edx' in v2 and i != 0x45: # avoid if last value in the block 
                        n = int(v2.split("*")[1].split("]")[0])
                        y = x*n
                        print("test: ", y, n, x)
                    elif 'lea ebx' in v2 and 'rax*' in v2:
                        n = int(v2.split("*")[1].split("]")[0])
                        x *= n
                    elif 'lea ebx' in v2:
                        print(v2)
                        # input('HI')
                        x += y
                    elif 'add eax, eax' in v2:
                        x *= 2
                    elif 'sub' in v2:
                        x -= 1
                    elif 'movsx' in v2:
                        flag2 = True
                        x = 1
                    elif 'add' in v2:
                        print(v2)
                        input("Found other")

                if flag2 == True:
                    mul_val = x 
            if pos != -1:
                new_b = Block(pos, mul_val)
                # print(f"Position: {new_b.pos}, mult val: {new_b.mul}")
                self.block_arr.append(new_b)
        print(len(self.block_arr))
         
    def to_vector(self):
        vector = [0] * 0x46
        for i,v in enumerate(self.block_arr):
            vector [v.pos] = v.mul
        return vector

    def check_all_rbx(self, vec, debug):
        # s is the running summary of  the rbx values we collected so far
        # 
        s = 0x0
        for i in range(70):
            if self.check_arr[i] != s and debug == 49:
                print(i-1, self.block_arr[i-1].pos, self.block_arr[i-1].mul)
                print("Running sum: ", hex(s))
                print("ebx extracted: ", hex(self.check_arr[i]))
                input("Discrepancy ")
            s += vec[i] * self.payload[i]

        return s

def main():
    chunks = get_chunks()
    print(len(chunks))
    # print([i.hex() for i in chunks])
    # input()
    # header = open('./header', 'rb').read()
    start_addr = 0x00005555555563BD
    
    matrix = []
    res = []
    for i in range(0, len(chunks)-1):
        get_assembly(chunks[i][5:])
        # chunk = header+chunks[i][5:] + b'\x39\xc2' # opcodes for cmp rdx, rax
        if i != 0:
            chunk = chunks[i][5:] + b'\x39\xc2' # opcodes for cmp rdx, rax
        else:
            chunk = chunks[i] + b'\x39\xc2'
        print(f"Start address for debugging: {hex(start_addr)}")
        s = solver(chunk, start_addr)
        start_addr += len(chunks[i]) + 8 # 8 for the extra opcodes that got cut
        s.run()
        # print(s.ops)
        s.split_to_blocks()
        v = s.to_vector()
        matrix.append(v)
        res.append(s.final_val)
        print("i is: ", i)
        print(v)
        print([hex(i) for i in v])

        check_val = s.check_all_rbx(v, i)
        # check_val = sum([v[i] * s.payload[i] for i in range(0x46)])
        print(f"My val: {hex(check_val)}, Correct val: {hex(s.check_me)}")
        assert check_val == s.check_me
        # input()
        # fixme.append(s.matrix[0])
        #
    A = np.array(matrix)
    b = np.array(res)
    inv = np.linalg.inv(A)
    print(A)
    print([hex(i) for i in b])
    print(np.linalg.det(A))
    print(A.shape)
    a = inv @ b
    print(a)
    a = np.around(a).astype(int)
    print(a)
    print(''.join([chr(i) for i in a]))


        
        # input("Running")
    

if __name__ == '__main__':
    main()
    # flag[ 87.  97.  82.  80. 123.  55.  48.  52.  55.  52.  56.  48.  99.  53.
 # 100.  55.  98.  99.  98.  55.  98.  49.  98. 101. 101.  98.  56.  54.
 #  55. 102.  56. 101.  56.  54. 100.  54.  55.  56.  53.  48.  56. 102.
 #  97.  48.  99.  49.  98.  49. 102. 102.  56.  49.  52.  54.  98.  54.
 #  99.  54.  97.  97. 101.  51.  53.  57.  51.  48. 102.  50.  48. 125.]

    # flagj 
# WaRP{7047480c5d7bcb7b1beeb867f8e86d678508fa0c1b1ff8146b6c6aae35930f20}


