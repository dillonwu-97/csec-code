import z3

def bitmix (chr):
    '''
    Accept some character
    generate new permutation based on the bits of the chr
    0 1 2 3 4 -> 4 3 1 2 0 
    '''
    # second half
    a = 2 * (chr & 4) 
    b = 2 * (chr & 8)
    c = (chr & 0x10) >> 2
    d = (a | b | c)
    second_half = (d & 0x1c) >> 2

    # first half
    a = (chr & 2) >> 1
    b = 2 * (chr & 1)
    c = (a | b) & 3
    first_half = 8 * c

    return first_half | second_half

def sandbox():
    temp2 = []
    for i in range(0x100):
        temp = bitmix(i)
        temp2.append(temp)
        print(f"orig:{i} mix:{temp}")
        print(f"orig:{bin(i)[2:][-5:]} mix:{bin(temp)[2:].zfill(5)}")
    print(len(set(temp2)))

# probably need to build out a sat solver
# only need to store the unique data_buf idx values 
# and then c2[idx_a] + inp[idx_b] is equal to this data_buf idx output 
# sat solver needs to do a lot of work though; needs to solve for 256^25?
# but it's just addition so maybe realistically solvable with a system of linear equations even 
# i have 25 equations
# each equation has additions between two numbers and mode 199

# there is a mismatch in the number of elements in each...
a_buf = [
    0xC2, 0x3F, 0x9C, 0x15, 0x7C, 0x19, 0x81, 0x47,
    0x1F, 0xB2, 0xC9, 0xA7, 0x46, 0x97, 0x3F, 0x8D,
    0x68, 0x0B, 0x7C, 0x31, 0x2A, 0x79, 0x49, 0x43,
    0x2D, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
]

# there are more bytes in this buffer than 25 so what are the extra bytes for, if anything?
b_buf = [
    0x08, 0xBA, 0xB6, 0x16, 0xC5, 0x4A, 0x1B, 0x27,
    0x0B, 0x95, 0x6A, 0x02, 0x91, 0x30, 0x6F, 0x81,
    0x6F, 0x80, 0x2B, 0x5D, 0xB6, 0xA5, 0x21, 0x83,
    0x10, 0x89, 0xA1, 0x66, 0x15, 0x93, 0x1A, 0x00
]

# expected values given the loop (i->5(j->5(k from 0->1.0, .2 )))
# inp z3 0->4 is result arr 0->4
result_arr = [
    8, 111, 11, 16, 182, 43, 106, 161, 197, 182, 
    145, 21, 27, 33, 111, 26, 186, 128, 149, 137, 
    22, 93, 2, 102, 74
]
a_buf_tuples = []
for i in range(5):
    temp = []
    for j in range(5):
        temp.append(j * 5 + i)
    a_buf_tuples.append(temp) 

def satsolve():

    # constructing the z3 solver now
    solver = z3.Solver()
    v = z3.Int('v')
    w = z3.Int('w')
    x = z3.Int('x')
    y = z3.Int('y')
    z = z3.Int('z')
    # this sat solver is taking too long, need more constraints i think 
    #
    # solver.add(v == ord('d'))
    # solver.add(w == ord('m'))
    # solver.add(x == ord('4'))
    # solver.add(y == 59)
    # solver.add(z == 38)
    # [x = 101, w = 42, v = 79, z = 38, y = 59]
    # [x = 34, w = 66, v = 125, z = 93, y = 118]
    # solver.add(z == ord('}'))
    solver.add(v >= 97, v <= 100)
    solver.add(w >= 97, w <= 120)
    solver.add(x >= 97, x <= 122)
    solver.add(y >= 97, y <= 122)
    solver.add(z >= 97, z <= 122)

    print(result_arr[i+5:i+10])
    for i in range(5): # 0 -> 5
        tbuf = a_buf_tuples[i]
                # solver.add(result_arr[i] == (\
        #                              (v * a_buf[tbuf[0]] % 199) +\
        #                              (w * a_buf[tbuf[1]] % 199) +\
        #                              (x * a_buf[tbuf[2]] % 199) +\
        #                              (y * a_buf[tbuf[3]] % 199) +\
        #                              (z * a_buf[tbuf[4]] % 199) % 199))
        constraint = (result_arr[i+5] == ((
                           (v * a_buf[tbuf[0]] % 199) +
                           (w * a_buf[tbuf[1]] % 199) +
                           (x * a_buf[tbuf[2]] % 199) +
                           (y * a_buf[tbuf[3]] % 199) +
                           (z * a_buf[tbuf[4]] % 199)) % 199))
        solver.add(constraint)
    print(solver.assertions())
    ok = solver.check()
    print(ok)
    if ok == z3.sat:
        print(solver.model())

def check(v, w, x, y, z):
        

    for i in range(5):  
        tbuf = a_buf_tuples[i]
        is_ok = (result_arr[i+20] == ((
                           (v * a_buf[tbuf[0]] % 199) +
                           (w * a_buf[tbuf[1]] % 199) +
                           (x * a_buf[tbuf[2]] % 199) +
                           (y * a_buf[tbuf[3]] % 199) +
                           (z * a_buf[tbuf[4]] % 199)) % 199)) 
        
        if is_ok == False:
            return False
    return True

def loopsolve():
    '''
    '''
    for v in range (32, 97):
        print("v", v)
        for w in range(33, 128):
            print("w", w)
            for x in range(33, 128):
                for y in range(33, 128):
                    # just for the last loop though
                    z = ord('}')
                    is_ok = check(v, w, x, y, z)
                    if is_ok == True:
                        print(v, w, x, y, z)
                        input("Found!") 
                    # for z in range(33, 128):
                    #     is_ok = check(v, w, x, y, z)
                    #     if is_ok == True:
                    #         print(v, w, x, y, z)
                    #         input("Found!")
                        # TODO: just do this instead of using z3
                        # no idea why z3 is so fucking slow 

def main():
    # sandbox()
    # satsolve()
    # first five characters could be DH{Th
    # can guess the last character but what about the ones in the middle?
    # [z = 104, y = 84, v = 68, w = 72, x = 123]
    #   [68, 72, 123, 84, 104]
    # [x = 34, w = 125, v = 100, z = 121, y = 99]
    #   [100, 125, 34, 99, 121]
    #
    # [x = 34, w = 66, v = 125, z = 93, y = 118]
    #   [125, 66, 34, 118, 93]
    #
    # [x = 101, w = 42, v = 79, z = 38, y = 59]
    # [x = 120, w = 124, v = 111, y = 121, z = 125]

    sol = [68, 72, 123, 84, 104]            # correct DH{Th}
    # sol += [100, 125, 34, 99, 121]  # wrong
    sol += [114, 52, 64, 100, 95] # correct r4Ad_

    # sol += [125, 66, 34, 118, 93]   # wrong
    sol += [109, 97, 116, 114, 49] # ['m', 'a', 't', 'r', '1']

    # sol += [79, 42, 101, 59, 38] # <-- double check I did this right too 
    sol += [120,95,109,48,100] # ['x', '_', 'm', '0', 'd']

    # sol += [120, 124, 111, 121, 125] # wrong
    sol += [95,49,57,57,125]
    print(''.join([chr(i) for i in sol]))
    # loopsolve()
    # DH{Thr4Ad_matr1x_m0d
    # DH{Thr4@d_matr1x_m0d_199}


if __name__ == '__main__':
    main()
