from pwn import *

def eval_exp(opstack, numstack):

    right = int(numstack.pop())
    left = int(numstack.pop())
    

    op = opstack.pop()
    if op == '*':
        ret = left * right
    elif op == '-':
        ret = left - right
    elif op == '+':
        ret = left + right
    else:
        ret = left // right
    return str(ret)


def solve(s):
    s = s.replace("(", "( ").replace(")", " )")
    l = s.split(" ")
    opstack = []
    numstack = []
    for i,v in enumerate(l):
        # print(v, numstack, opstack)

        # handle nums
        if v.isnumeric():
            numstack.append(v)
            if (len(opstack) > 0 and opstack[-1] in "+/"): # high priority
                out = eval_exp(opstack,numstack)
                numstack.append(out)
        elif v in "*/+-":
            opstack.append(v)
        elif v == "(":
            opstack.append(v)
            continue
        elif v == ")":
            while(len(opstack) > 0 and opstack[-1] != "("):
                out = eval_exp(opstack, numstack)
                numstack.append(out)
            opstack.pop()
            if (len(opstack) > 0 and opstack[-1] in "+/"): # high priority
                out = eval_exp(opstack,numstack)
                numstack.append(out)
        else:
            continue

    # solve the rest
    while (len(numstack) > 1):
        out = eval_exp(opstack, numstack)
        numstack.append(out)
    return numstack[0]

def sandbox():
    print(solve("1 + 2 * 3")) #9 
    print(solve("(52 + 68) * 86"))
    print(solve("65 * (86 * 100) * 97 * 48 * 33"))
    print(solve("(9 + 1 * 52 * 6 * 94 * 45 + 61 * 84)"))

def main():
    r = remote('167.172.62.51', 31359)
    for i in range(500):
        l = r.recvuntil("?").decode()
        print(l)
        l = l.split(']: ')[1].split(" =")[0]
        print(l)
        ans = solve(l)
        print(ans)
        l = r.recvuntil("> ")
        print(l)
        r.sendline(ans)
    r.interactive()
    # Flag: HTB{tH0s3_4r3_s0m3_k1llEr_m4th_5k1llz}



if __name__ == '__main__':
    main()
    # sandbox()
