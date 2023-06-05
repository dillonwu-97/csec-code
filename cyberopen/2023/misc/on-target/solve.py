from pwn import *
from base64 import *
from requests import *
from Crypto.Util.number import bytes_to_long, long_to_bytes
from ast import literal_eval
import math

def attack(r, payload):
    l = r.sendline(str(payload))
    l = r.recv()
    return l

def dist(tx, ty, mx, my):
    '''
    tx = target x, ty = target y, mx = candidate x, my = candidate y
    '''
    return math.sqrt((tx - mx) ** 2 + (ty - my) ** 2)

def failed(guesses, resp):
    print("[*] Triangulating")
    best_x = None
    best_y = None
    best_val = 1000
    for i,v in enumerate(resp):
        if v < best_val:
            best_val = v
            best_x = guesses[i][0]
            best_y = guesses[i][1]

    zero_val = resp[0] # return value when sending 0
    zero_dist = zero_val * zero_val # distance, tx^2 + ty^2 
    best_dist = best_val * best_val # distance, (tx - bestx)^2 + (ty - besty)^2, tx^2 + ty^2 - 2*tx*mx - 2*ty*my + mx^2 + my^2
    temp2 = best_dist
    best_dist -= zero_dist
    best_dist -= best_x ** 2
    best_dist -= best_y ** 2
    best_dist //= (-2)

    best_guess_x = None
    best_guess_y = None
    best_guess_val = 10000000000000
    print(best_dist)
    for i in range(1000):
        for j in range(1000):
            temp = abs(best_dist - (best_x * i + best_y * j)) 
            if temp < best_guess_val:
                best_guess_val = temp
                best_guess_x = i
                best_guess_y = j
    print("best guesses: ", best_guess_x, best_guess_y, )
    print(temp2, best_guess_x**2 + best_guess_y**2)
    return best_guess_x, best_guess_y


def failed2(to_send, resp):
    print("[*] Triangulating")
    best_x = 0
    best_y = 0
    best_guess = 1000000000
    for i in range(1000):
        #print("i:", i)
        for j in range(1000):
            total = 0
            for k, v in enumerate(resp):
                if k == 5:
                    break
                expected_val = dist(i, j, to_send[k][0], to_send[k][1]) # tx, ty, mx, my
                total += abs(resp[k] - expected_val)
            if (total < best_guess):
                best_guess = total
                best_x = i
                best_y = j
    return best_x, best_y


def triangulate(guesses, resp):
    best_guess = None
    best_val = 1000000
    for i, v in enumerate(resp):
        if v < best_val:
            best_val = v
            best_guess = i

    to_send = []
    new_x = guesses[best_guess][0]
    new_y = guesses[best_guess][1]
    for i in range(10):
        r = random.randint(0,4)
        if r == 0:
            new_send = [new_x + 5, new_y + 5]
        elif r == 1:
            new_send = [new_x + 5, new_y - 5]
        elif r == 2:
            new_send = [new_x - 5, new_y - 5]
        else:
            new_send = [new_x - 5, new_y + 5]
        to_send.append(new_send)
    return to_send


        





def sandbox():
    r = remote('0.cloud.chals.io', 32121)
    #l = r.recvuntil("coordinates: \n\n")
    l = r.recvuntil("coordinates:")
    print(l)
    l = r.recvline()
    l = r.recvline()


    to_send = []
    x = 500
    y = 500
    # triangulation requires two coordinates?
    # math is target_x - my_x) ^ 2
    for i in range(5):
        to_send.append([x,y])
        x -= 10
        y += 10
    x = 500
    y = 500
    for i in range(5):
        x += 10
        y -=10
        to_send.append([x,y])
        
    for i in range(10):
        print(to_send)
        print("index: ", i)
        resp = attack(r, to_send)
        print(resp)
        to_send = triangulate(to_send, literal_eval(resp.decode()))

def main():
    print("[*] Starting solve")
    sandbox()
    # USCG{g0t_1t_1n_my_s1t35}

if __name__ == '__main__':
    main()


