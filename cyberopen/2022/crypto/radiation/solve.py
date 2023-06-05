import random
from collections import Counter
from z3 import *

mask = (1 << 64) - 1

with open("bip39.txt") as f:
    bip = [i for i in f.read().split("\n") if i]


def convert_to_string(token):
    r = token
    n = []
    for i in range(6):
        n.append(token & 0x7FF)
        token >>= 11
    return "-".join([bip[i] for i in n])


print("*" * 10 + "Starting solve" + "*" * 10)
##### Step 1 #####
# Get the corresponding index for each word
d = {}
for i,v in enumerate(bip):
    d[v] = i

##### Step 2 #####
# Get the list of tokens as binary strings
word_chains = open('./tokens.txt', 'r').read().split("\n")
seeds_list = []
for i,v in enumerate(word_chains):
    if v == '': continue
    print(f'Iteration: {i}, Value: {v}')
    words = v.split("-")
    nums = [d[w] for w in words][::-1] # need to reverse because the first word is generated from the rightmost values
    bi = [bin(n)[2:].zfill(11) for n in nums] # each number is 11 bits
    token = int(''.join(bi), 2)
    print(f"token is: {token}")
    seeds_list.append(token)
assert(len(seeds_list) == len(word_chains)-1)

# Get the increment value list
# seeds_list[0] corresponds to the first word_chain
# seeds_list[8] = inc_list[0]
# First 64 bits is used for the rightmost value
inc_list = []
for i in range(8, len(seeds_list)):
    inc_list.append(seeds_list[i])

# Verifying that it works
for i,v in enumerate(seeds_list):
    assert(convert_to_string(v) == word_chains[i])

# Create longseed list
longseed = []
for i in range(0, len(seeds_list)-8):
    ls = seeds_list[i:i+8][::-1] # Need to reverse before rightmost val comes first
    bi = ''.join([bin(n)[2:].zfill(64) for n in ls])
    longseed.append(int(bi,2))
print(longseed)

# Verifying that the longseed values are correct
for i,v in enumerate(longseed):
    # print(f"Iteration: {i}, Value: {v}")
    assert (v & mask == seeds_list[i])

assert(len(inc_list) == len(longseed))
# # Using z3 to solve for state_1 and state_2 value
s = Solver()
s1 = BitVec("s1", 64)
s2 = BitVec("s2", 64)
def z3_solve(result, seed):
    return ( (result * s1 + ((s1+s2)&mask) ) ^ seed) & mask

for i in range(len(inc_list)):
    seedy = longseed[i] >> 64
    s.add(inc_list[i] == z3_solve(seeds_list[i], seedy))
if s.check() == sat:
    print(s.model())

# z3 output
# [s2 = 10232235694175749026, s1 = 336801044331229251]
seed = longseed[0]
state1 = 336801044331229251
state2 = (state1 + 10232235694175749026) & mask


def generate_token():
    global seed, state1, state2, mask
    # print("Starting seed: ", bin(seed))
    # print("Starting mask: ", bin(mask))
    result = seed & mask
    # print("Result: ", bin(result))
    seed >>= 64
    # print("Seed after right shift 64: ", bin(seed))
    inc = ((result * state1 + state2) ^ seed) & mask
    # print("Increment value: ", bin(inc))
    seed |= inc << (7 * 64)
    # print("Inc val shifted: ", bin(inc << 7 * 64)[2:])
    # print("Final seed: ", seed)
    return result

print("\n".join(["  " + convert_to_string(generate_token()) for i in range(0, 31)]))
# flag{shouldnt_have_used_my_own_number_generator}


