read 0x50 into the buffer 
leak somewhere?
read 0x40 bytes into the buffer?
But to what end?
rdi = rsi
i think i can overwrite 2 bytes 
overwrite got value to point somewhere else?
maybe rop chain build?
can't leak system, but i can replace strcmp with printf and call printf with an argument to do fprintf leak i think 
Not sure why the leak works 


so build rop chain 
call printf on a leak to the base of libc 
then do a second write? 
not sure if i have arbitrary write either 
call printf to do %s possibly 
i think i need to get a libc leak? 


need to call read 
rdi = 0x0 
rsi = buffer
rdx = bytes to read 

stack pivot again 
