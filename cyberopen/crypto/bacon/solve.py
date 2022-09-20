from pwn import *
#from scapy.all import *
import ast
import math


def main():

    STAGE = 2
    if STAGE == 1:
        pcapfile = './beacon.pcapng'
        rfile = rdpcap(pcapfile)
        data = []
        for packet in rfile:
            temp = bytes(packet[UDP].payload)
            d = ast.literal_eval(temp.decode('utf-8'))
            data.append(d)


        print(data)
        f = open('./messages.txt', 'w')
        f.write(str(data))
        f.close()

    if STAGE == 2:
        f = open('./messages.txt', 'r').read()
        data = ast.literal_eval(f)
        print(data)
        n_vals = []
        for i in data:
            n_vals.append(i["n"])
       
        factors = []
        for i in range(0, len(n_vals)):
            for j in range(i+1, len(n_vals)):
                factor = math.gcd(n_vals[i], n_vals[j])
                if factor != 1:
                    factors.append( (factor, i, j) )
        for i in factors:
            print(i)

        factor = factors[0]
        p = factor[0]
        m1 = factor[1]
        m2 = factor[2]
        
        # m^e mod n = c
        # c^d mod n = p
        # d = mod_inv(e, phi(n))

        x1 = data[29]
        p1 = p
        q1 = x1['n'] // p1
        assert (q1 * p1 == x1['n'] and x1['n'] % q1 == 0)
        e1 = x1['e']
        d1 = pow(e1, -1, (p1 -1) * (q1 - 1))
        print("d1 is: ", d1)
        cipher = x1['msg']
        plain = str(pow(cipher, d1, x1['n']))
        ret1 = ''
        assert (pow(int(plain), e1, x1['n']) == cipher)
        print(plain)
        for i in range(0, len(plain), 2):
            temp = plain[i:i+2]
            #print(int(temp), chr(int(temp)))
            ret1 += chr(int(temp, 16))


        temp = hex(int(plain))
        print(bytes.fromhex(temp[2:]).decode('utf-8'))
        # USCG{C0mm0n_f@ct0r5_FtW}


if __name__ == '__main__':
    main()
