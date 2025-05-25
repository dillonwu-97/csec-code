# Radiation Leak Writeup

This challenge was a cryptography challenge for the 2022 US Cyber Games CTF. The objective is to correctly ascertain the next sequence of words that are needed to login to the website. We have the source code that is used to generate the phrases as well as a history of the phrases. 

### Function Descriptions

convert_to_string()
This function is relatively straightforward. It takes some token value and then separates the token into six different 11 bit blocks. Each of these 11 bit blocks is an index into the BIP39 list of words. 

generate_token()
This function creates the token used for passphrase generation. It uses several values that are declared globally and updates them. These globals include seed, state_1, and state_2. If we have the initial state of these globals, we can replicate the passphrase generation process. 

The objective is thus to get state_1, state_2, and seed. 

### Step 1: BIP39
First, we have to obtain the source of the words used to generate the tokens from the leaked_tokens.txt file. BIP39 is a reference to a word list used for producing mnemonic codes or encryption keys for cryptocurrency wallets, and is openly available online. We can download the wordlist. 

```
with open("bip39.txt") as f:
    bip = [i for i in f.read().split("\n") if i]
d = {}
for i,v in enumerate(bip):
    d[v] = i
```

### Step 2: Seeds
Now that we have the word list, we can use it to extract all of the tokens that were used. This is because all of the words in the BIP39 list are unique; we can use each passphrase to obtain the corresponding index of the word from the BIP39 list. We can join these indices to reconstruct the original token value, which in turn gives us the seed values. We now have a list of all the seed values that were used called seeds_list.

For example, the first passphrase is friend-border-cinnamon-laundry-shoot-chronic.  
The index for these values is 743-206-328-1005-1588-323.  
We have to reverse these index values because the first word is generated from the rightmost values: 323-1588-1005-328-206-743.   
When we join the 11 bit binary representatino of each number, and we get 11665246462824313575.  

```
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
```

### Step 3: Inc 
There is an intermediate variable inc in the generate_token() function which utilizes state_1 and state_2. This value is important because if we have the inc values, we can use the sat solver z3 to obtain state_1 and state_2. From the second to last line in the generate_token() function, we can observe that we actually do have all of the inc values. Each new 64 bit inc variable is appended to the start of the 448 bit seed value. This implies that the seeds_list[8] = inc_list[0]. 

```
inc_list = []
for i in range(8, len(seeds_list)):
    inc_list.append(seeds_list[i])

longseed = []
for i in range(0, len(seeds_list)-8):
    ls = seeds_list[i:i+8][::-1]
    bi = ''.join([bin(n)[2:].zfill(64) for n in ls])
    longseed.append(int(bi,2))
```

### Step 4: state_1 and state_2
With a list of the intermediate inc values, we can finally use z3 to obtain state_1 and state_2. With state_1 and state_2, we are able to obtain the next passphrase used to login to the website by running the provided script.

```
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
```

The passphrase is: tool-unveil-ranch-soldier-coast-cover  
The flag is: flag{shouldnt_have_used_my_own_number_generator}