 # for each hex in message
 # subtract 18 on both sides mod 256
 # find x by using mod inverse

import gmpy2

def main():
    f = open('msg.enc', 'r').read()
    print(f)
    a = []
    for i in range(0,len(f), 2):
        temp = int(f[i: i+2],16)
        a.append(temp)

    # y = (123 * x + 18) % 256

    n = gmpy2.invert(123, 256)
    flag = ''
    for i in a:
        c = (i - 18) % 256
        c *= n
        c %= 256

        # print(c)
        assert ((123 * c + 18) % 256 == i)
        # if ()
        # print(i, (123 * (c % 256) + 18) % 256, c % 256)
        flag += chr(c)
 
    print(flag)
        


        

if __name__ == '__main__':
    main()