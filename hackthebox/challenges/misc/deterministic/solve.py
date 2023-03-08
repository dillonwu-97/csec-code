
def print_loop(d, start):
    temp = start
    for i in range(1000):
        print(temp)
        temp = d[temp]

# Find the path to 999
def find_path(d, start):
    global path, seen
    path = []
    seen = []
    def find(val):
        global path, seen
        #print(f"val is {val}")
        if val == 999:
            return True
        elif val not in d or val in seen:
            return False
        else:
            prev = val
            seen.append(val)
            for i,v in enumerate(d[val]):
                val = v
                ok = find(val)
                if not ok:
                    path = path[:-1]
                else:
                    path.append(str(prev) + " " + str(val))
                    return True
            return False
        return False
    ret = find(start)
    print(path)
    return path

def get_chars(middle, path):
    ret = []
    for i in path:
        ret.append(middle[i])
    return ret
        

'''
The states are correct but just for security reasons, 
each character of the password is XORed with a very super secret key.
Note: there are multiple values for each key, i.e. repeats

Idea: There are multiple paths to 999. Find the one that leads there.
Afterwards, extract all of the middle values and that is probably the ciphertext of the flag
Find the xor key using brute force
'''
def solve():
    f = open('./deterministic.txt','r').read()
    nums = set(f.split('\n'))
    print(nums)
    start = 69420
    d = {}
    middle = {}
    for i,v in enumerate(nums):
        n = v.split(' ')
        a,c = int(n[0]),int(n[2])
        if a in d:
            print('Found left dup: ', a)
            d[a].append(c)
        else:
            d[a] = [c]

        middle[str(a) + " " + str(c)] = n[1]

    path = find_path(d, start)
    path = path[::-1]
    print(middle)

    c_arr = get_chars(middle, path)
    c_arr = [int(i) for i in c_arr]
    print(c_arr)

    for k in range(1,256):
        print("k is: ", k)
        s = ''.join([chr( (i^k) ) for i in c_arr])
        print(s)
        if 'HTB' in s:
            input()
        print("*" * 10)

def test():
    pass

def main():
    solve()
    test()
    # Flag: HTB{4ut0M4t4_4r3_FuUuN_4nD_N0t_D1fF1cUlt!!}

if __name__ == '__main__':
    main()    


