from numpy import true_divide
from pwn import *
from collections import Counter
import json
import base64

NOT_CHAR = 1
IS_CHAR = 0

def get_character(t, row):
    for i,v in enumerate(t[row]):
        if v == IS_CHAR:
            return chr(i)
    
    return None

# Check how many unchecked characters there are remaining
# There are 12 characters we need to brute force
def check_table(t, row):
    c = Counter(t[row])
    if c[IS_CHAR] == 1:
        temp = get_character(t, row)
        print(f"Found character {temp} for index {row}")
        return True
    else:
        return False

def check_all(t):
    for i in range(7,20):
        if check_table(t, i) == False:
            return False
    return True

# Construct the initial table 
def construct_table():

    # row = flag, column = character
    t = [[0 for i in range(256)] for j in range(20)]
    assert(len(t) == 20)

    flag_start = 'crypto{'
    for i in range(7):
        for j in range(256):
            if j != ord(flag_start[i]):
                t[i][j] = NOT_CHAR
    
    flag_end = '}'
    for j in range(256):
        if j != ord(flag_end):
            t[-1][j] = NOT_CHAR
        
    return t

def populate_table(t, c):
    for i,v in enumerate(c):
        t[i][v] = NOT_CHAR

def progress(t):
    for i,v in enumerate(t):
        print(Counter(v))

def construct_flag(t):
    flag = ''
    for i,v in enumerate(t):
        c = get_character(t, i)
        flag += c
    return flag

def main():
    r = remote('socket.cryptohack.org', 13370)
    t = construct_table()

    r.recvuntil("leaks\n")
    counter = 0
    while (check_all(t) == False):
        if counter % 1000 == 0:
            print(f"Flag is: {construct_flag}")
        counter += 1
        r.sendline(json.dumps({"msg":"request"}))
        l = json.loads(r.recvline().strip().decode())
        print(l)
        if "error" not in l:
            ciphertext = base64.b64decode(l['ciphertext'])
            populate_table(t, ciphertext)
            # print(f"Ciphertext: {ciphertext}")
        else:
            print(f"Progress report: ")
            progress(t)
    print(construct_flag(t))
        
    # crypto{unr4nd0m_07p}

    


if __name__ == '__main__':
    main()