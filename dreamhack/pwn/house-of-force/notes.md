The conditions for the exploit are to be able to control the size of the top chunk?
need to figure out a way to build an arbitrary write primitive from this
overwrite got exit with the address for shell 
need to get a pointer to the exit_got 
1) overwrite the wilderness address area with -1 
2) the next heap allocation will be offset from this value 


can only write once in this challenge it seems 

When we do an alloc, we get the address and then subtract from it to get a new pointer 
but where is the start?
need to get the formula
got malloc corrupted top size 

- [ ] Find unpatched version of glibc 
- [ ] use it for the exp and calculate from -1 to exit got 


- https://elixir.bootlin.com/glibc/glibc-2.29/source/malloc/malloc.c
the patch was introduced in glibc 2.29

/pwn/house-of-force/glibc/glibc-2.28/build$ make -j$(
nproc) --disable-werror --enable-cet
cet = control flow enforcement technology
building gives an error related to se linux\
might be easier to just use docker 
the house of force file is 32 bit binary??


nb is the requested size?
3 mallocs, second to change


yea i dont think i actually need to set it to -1 just to the main arena address
right the idea is that the top chunk stores the size so making it very large means we wont expand the top chunk heap 


for simple chunks, let's think about what happens
if 0x60 
heap address gets incremented, size gets decremented 
so to get to our write address, it is smaller, so we need to submit a negative value 
