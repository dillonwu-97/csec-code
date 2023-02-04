from pwn import *

def main():
    r = remote('mc.ax', 31493)
    for i in range(128):
        if i % 8 == 0:
            print("iter: ", i)
        m0 = '00' * 16
        m1 = '11' * 16


        # Receive and use option 1
        r.recvuntil('Action: ')
        r.sendline('1')
        r.recvuntil(': ')
        r.sendline('00' * 16)
        l = r.recvuntil(': ')
        r.sendline('11' * 16)
        enc = r.recvline()

        # Use option 2 to decode
        l = r.recvuntil('Action: ')

        r.sendline('2')
        l = r.recvuntil('hexstring): ')
        enc = enc.decode().zfill(512)
        r.send(enc)
        dec = r.recvline()
        l = r.recvuntil(': ')

        # Option 0 now
        if dec.decode().strip() == m0:
            guess = '0'
        else:
            guess = '1'

        r.sendline('0')
        l = r.recvuntil(': ')
        r.sendline(guess)
        l = r.recvline()



    l = r.recvline()
    print(l)
            

    

if __name__ == '__main__':
    main()
