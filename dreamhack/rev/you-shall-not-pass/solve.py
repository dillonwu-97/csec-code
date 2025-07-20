def xor(arr):

    '''
    forward function, need to reverse this
    '''
    for i in range(len(arr)-1):
        temp = arr[i] ^ arr[i+1]
        temp = temp & 0xffff
        assert temp > 0
        arr[i] = temp
    print(arr)
    input("After xor")
    return arr

def and_arr(arr): # arr is user input
    # need to check if this is actually correct
    # how reverse this, looks like linear cipher or something along those lines
    # so the last one is at position 0 
    # this must be wrong; it cannot be an inplace modification 
    # i need to review the array ops for this 
    mask = 31
    new_arr = [-1] * 32
    sz = 32 
    for i in range(31, -1, -1):
        diff = sz - i - 1 
        temp = mask & diff # mask the diff with 0xffff
        sum = arr[i] + arr[mask & (i-1)] # not sure if this negative value is correct
        print(f"diff: {diff}, i:{i}, mask_and_i_min_1: {mask & (i-1)}" )
        # there is no operation applied to the sum value to make it more usable...
        # sum &= 0xffff
        new_arr[temp] = sum 
        # new_arr[temp] %= 256

    print(new_arr)
    print("after and")
    return new_arr

def rev_and(old_arr):
    mask = 31
    sz = 32
    new_arr = [-1] * 32
    new_arr[31] = old_arr[31] - old_arr[0]
    new_arr[31] &= 0xffff
    # new_arr[31] %= 256 # not sure if this should be here in truth
    # new_arr[31] &= 31
    for i in range(30, -1, -1):
        new_arr[i] = old_arr[30 - i] - new_arr[i + 1] # TODO: this could be wrong
        new_arr[i] &= 0xffff
        # new_arr[i] %= 256
    print("new arr: ", new_arr)
    return new_arr
    
def rev_xor(arr):
    # arr[-1] %= 256
    # arr[-1] &= 0xffff
    for i in range(len(arr) - 1, 0, -1):
        temp = arr[i-1] ^ arr[i]
        temp &= 0xffff
        arr[i-1] = temp
        # assert temp > 0
        # assert temp < 256 and temp >0
        # print(arr[i-1])
    print("after rev xor: ",arr)
    # input()
    return arr

'''
Equations:
new_arr[31] = old_arr[31] - old_arr[0]
new_arr[30] = old_arr[0] - new_arr[31]
new_arr[29] = old_arr[1] - new_arr[30]
.
.
.
new_arr[0] = old_arr[30] - new_arr[1]

'''

def forward(arr):
    a1 = xor(arr)
    a2 = and_arr(a1)
    return a2

def backward(arr):
    a1 = rev_and(arr)
    a2 = rev_xor(a1)
    return a2




def solve():
    
    a = ord("D")
    b = ord("H")
    c = ord("{")
    d = ord("}")

    a1 = [-1] * 32
    a1[0] = a ^ b
    a1[1] = b ^ c
    a1[31] = d

    a2 = [-1] * 32
    a2[30] = a1[0] + a1[1]
    a2[31] = a1[0] + a1[31]
    print(a2[30], a2[31])
    
    correct = [
        148, 27, 14, 27, 34, 25, 10, 30, 48, 33,
        23, 15, 19, 43, 46, 30, 23, 15, 19, 43,
        33, 34, 60, 54, 49, 47, 42, 42, 51, 80,
        63, 137
    ]

    # something is wrong here
    # i am supposed to be recovering a1 and a0, a0 being the original values
    # a2 array and correct array are essentially the same arrays
    def helper(a1):
        for i in range(30, 1, -1):
            assert correct[30-i] != -1
            assert a1[i+1] != -1
            a1[i]  = correct[30 - i] - a1[i+1]
        return a1
    
    a1 = helper(a1)
    print(a1)
    a0 = [-1] * 32
    a0[0] = a
    a0[1] = b
    a0[2] = c
    a0[31] = d
    for i in range(2,31):
        a0[i+1] = a1[i] ^ a0[i]
        # a0[i] %= 256
    print(''.join([chr(i) for i in a0]))


    

def main():
    solve()

def sandbox():
    correct = [
        148, 27, 14, 27, 34, 25, 10, 30, 48, 33,
        23, 15, 19, 43, 46, 30, 23, 15, 19, 43,
        33, 34, 60, 54, 49, 47, 42, 42, 51, 80,
        63, 137
    ]
    # and_arr(correct)
    # a1 = rev_and(correct)
    # print(a1)
    # a2 = rev_xor(a1)
    # print(a2)

    rev_correct = backward(correct)
    print("checking!!!")
    print("rev correct: ", rev_correct)
    print([chr(i) for i in rev_correct])
    input("forward now")
    check_val = forward(rev_correct)
    # check_val = [i % 256 for i in check_val]
    print("correct: ", correct)
    print("check_val:", check_val)
    print(''.join([chr(i) for i in correct]))

    input()

    assert check_val == correct
    #
    # print("solution: ")
    # a2 = backward(correct)
    # print(a2)
    # print(''.join([chr(i) for i in a2])) # no way 
    # assert len(a2) == 32

    # so first thing is xor
    #
    # "}" = 125

# You can verify the length
# print(len(arr)) # Should be 32
# maybe there is something in the memcmp I am missing???
# not exactly sure how I would step through this even but I feel that I am close to solving the problem. Maybe I should double check my implementation

if __name__ == '__main__':
    main()
    # flag
    #DH{fpdrksmswjdakfwjdakfrnldudnj}

