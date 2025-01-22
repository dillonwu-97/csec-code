1) We need to get a leak 
trick is to use the create option
there is no error checking 
scanf returns an error 
but not sure what memory got dumped out from the stack 
ok have an address to libc 
gotta remember the last bit is previous_chunk_in_use



Would be useful to come up with a timeline of newly introduced malloc protections based on glibc and the heap 

https://sourceware.org/glibc/wiki/Glibc%20Timeline

For this exploit, we are on 2.36 and House of Eirenjar (sp) is dead


Building virtualbox on wsl if it's even possible lol 

house of einherjar no longer works because of the unlink check? 

there was also a format string vuln i missed in sell_picture

libc_leak -> get heap leak 

how to get the stack leak?

okay for the heap leak, we need to make sure the chunks are separated, otherwise they will consolidate
for the unsorted bin, coalescing happens immediately it seems 

https://elixir.bootlin.com/glibc/glibc-2.36/source/malloc/malloc.c#L4416
4597 contains the code for where we fault when we use a bad chunk 
fd pointer needs to be something valid, backwards pointer needs to be something valid i think 
this house should give us an arbitrary pointer in theory so we can go into libc system using it?

Problems:
How to force it to contain null bytes if there is a 0 check at each step?
we would have to use transform to modify the data inside it that already existed?
so overflow the next chunk
free the first chunk again 
reallocate the first chunk with smaller data using the same trick as before and then write bytes 
so sub goal is to control fd / bk pointer
i feel like we can only modify the bk pointer?

-> i think a forward coalesce happens when we free 0 instead of 1
-> backwards coalesce happens when we free 1 instead of 0
-> double free occurs when freeing 0
-> seg fault occurs when freeing 1

what is the problem?
the problem is that i dont understand how coalesce / unlink work very well 
very tricky and a lot of protections are added to it 
two paths forward: either we dont fail the double free check or we dont seg fault when doing the coalesce/unlink operation 
we get a new line and a 0 so we can push that then do a transform on a specific byte to make it 7f or something
what if we keep on overflowing backwards so something like what have now, so cascade backwards somehow 

bk pointer of one of the chunks needs to point to the stack
what happens after?
coalesce happens so the stack gets clobbered, and the next allocation we get gives us a pointer to the stack i think 
with a pointer to the stack, we can do a ret 2 libc / rop chain?
what about the canary / heap pointer? why did we need the heap leak 
i might have misunderstood something but we'll see 
- [ ] fix the stack pointer




