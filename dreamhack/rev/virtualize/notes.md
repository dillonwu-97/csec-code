need it to print out the flag based on some provided input


in order to update
sed -i 's|http://.*archive.ubuntu.com|http://old-releases.ubuntu.com|g' /etc/apt/sources.list
sed -i 's|http://.*security.ubuntu.com|http://old-releases.ubuntu.com|g' /etc/apt/sources.list
apt-get update
apt-get install -y python3


 0x401243 main
 0x4013EF addition
3 0x401935 xor
 0x401BD8 xor
 0x401E6E left shift
6 0x402104 right shift
7 0x40228B memcmp
8 0x4024DB exit
9 0x402511 read
a 0x402612 write
b 0x402713 free


─────────────[ REGISTERS / show-flags off / show-compact-regs off ]─────────────
*RAX  8
 RBX  0
 RCX  0x407120 ◂— 0x8493e3e6f22cfe2
*RDX  8
 RDI  7
*RSI  0x407160 ◂— 0x4b6f4d6d2c11e9f6
 R8   0x4082a0 ◂— 0x408
 R9   0x7ffff7fd9d00 ◂— endbr64 
 R10  0xfffffffffffff5c4

─────────────[ REGISTERS / show-flags off / show-compact-regs off ]─────────────
*RAX  8
 RBX  0
 RCX  0x407120 ◂— 0x8493e3e6f22cfe2
*RDX  8
 RDI  7
*RSI  0x407160 ◂— 0x4b6f4d6d2c11e9f6
 R8   0x4082a0 ◂— 0x408
 R9   0x7ffff7fd9d00 ◂— endbr64 
 R10  0xfffffffffffff5c4
 R11  0x5c464a799d510073
 R12  0x7fffffffdd48 —▸ 0x7fffffffe0b9 ◂— '/home/darklaw/Desktop/csec-code/dream
hack/rev/virtualize/shared/main_patched'
 R13  0x4011d6 ◂— endbr64 
 R14  0
 R15  0x7ffff7ffbc40 (_rtld_global_ro) ◂— 0x50fb200000000
*RBP  0x7fffffffdc20 ◂— 1
*RSP  0x7fffffffdbf0 —▸ 0x7fffffffdc20 ◂— 1
*RIP  0x402472 ◂— mov rdi, rcx


*RAX  8
 RBX  0
 RCX  0x407120 ◂— 0x8493e3e6f22cfe2
*RDX  8
 RDI  7
*RSI  0x407160 ◂— 0x4b6f4d6d2c11e9f6
 R8   0x4082a0 ◂— 0x408
 R9   0x7ffff7fd9d00 ◂— endbr64 
 R10  0xfffffffffffff5c4
 R11  0x1df34dd8b1e64e5b
 R12  0x7fffffffdd48 —▸ 0x7fffffffe0b9 ◂— '/home/darklaw/Desktop/csec-code/dream
hack/rev/virtualize/shared/main_patched'
 R13  0x4011d6 ◂— endbr64 
 R14  0
 R15  0x7ffff7ffbc40 (_rtld_global_ro) ◂— 0x50fb200000000
*RBP  0x7fffffffdc20 ◂— 1
*RSP  0x7fffffffdbf0 —▸ 0x7fffffffdc20 ◂— 1
*RIP  0x402472 ◂— mov rdi, rcx


R11 is random?
Doesn't seem like input affects it

maybe need to watch changes to these two positions
0x407160
0x407120

0x407120:       0x08493e3e6f22cfe2      0x4eb4affd83ef5c5c
0x407130:       0x08493e3e6f22ebe2      0x4eb4affd83ef5c5c
0x407140:       0x08493e3e6f22cfe2      0x4e14affd83ef5c5c
0x407150:       0x08493e3e6f22cfe2      0x4eb4affd83ef5c5c
0x407160:       0x4b6f4d6d2c11e9f6      0xdd03bc6ec5c92fdf
0x407170:       0x2e1a3d180c368bf4      0x3da2b98ea7bc6a4a
0x407180:       0x1e0f5a1d0b1618f6      0x6d30b9cb90f9783a
0x407190:       0x5c0d282d5c31d9c6      0x78a2ecab80a94a7f

0x000000000000a014 
after 
bytes get swapped so 0x41 -> 0x14
then it gets moved around in memory
then maybe it gets xored with some constants?

0x4b6f4d6d2c11e9f6      0xdd03bc6ec5c92fdf
0x407170:       0x2e1a3d180c368bf4      0x3da2b98ea7bc6a4a
0x407180:       0x1e0f5a1d0b1618f6      0x6d30b9cb90f9783a
0x407190:       0x5c0d282d5c31d9c6      0x78a2ecab80a94a7f
this is most likely the thing we need to be correct

can i do a gdb script to watch the dump being changed at each breakpoint until memcpy? is it worth it?
i can track 0's in the payload and map each out maybe

0x08493e3e6f22cfe2      0x4e80affd83effc5c
0x407130:       0x08493e3e6f22db86      0x4eb4affd83bb5c5c
0x407140:       0x8c497a3e6f22cfe2      0x4e90dbfd83ef5c5c
0x407150:       0x08493e3e6f22cfe2      0x4eb4affd83ef5c5c

64 character payload?

should i try to keep track of multiple?
let's try the payload with 0x41 on all of them and see if the output is the same
it is not a one to one mapping, there are other cascading effects I guess?

with input: AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB
0x407120:       0x2c5d1a1a4b36ebc6      0x6aa08bd997cb4878
0x407130:       0x1c6d2a1a7b36dbf6      0x6aa08be9a7fb4878
0x407140:       0x1c6d2a2a7b36ebc6      0x5aa0bbe9a7cb7848
0x407150:       0x2c5d1a2a4b06ebc6      0x5a90bbe997cb7848

C * 32, B * 32
0x407120:       0x2c0d1a1a4b66ebc6      0x6af08bd9c7cb1878 <-- 9c7 instead of 997
0x407130:       0x4c6d7a1a2b668ba6      0x6af08bb9a7ab1878
0x407140:       0x4c6d7a7a2b66ebc6      0x0af0ebb9a7cb7818
0x407150:       0x2c0d1a7a4b06ebc6      0x0a90ebb9c7cb7818

Z * 32, B * 32
0x407120:       0x2cec1a1a4b87ebc6      0x6a118bd926cbf978
0x407130:       0xad6d9b1aca876a47      0x6a118b58a74af978
0x407140:       0xad6d9b9bca87ebc6      0xeb110a58a7cb78f9
0x407150:       0x2cec1a9b4b06ebc6      0xeb900a5826cb78f9

alternating A/B
0x407120:       0x2c6d1a2a4b06dbc6      0x5aa08bd9a7cb4848
0x407130:       0x2c5d1a2a4b36dbc6      0x6aa0bbe997fb4878
0x407140:       0x2c5d1a1a4b36ebc6      0x5a90bbe9a7cb7848
0x407150:       0x2c5d2a1a4b36dbf6      0x5aa08bd997fb4878

0x407160:       0x4b6f4d6d2c11e9f6      0xdd03bc6ec5c92fdf
0x407170:       0x2e1a3d180c368bf4      0x3da2b98ea7bc6a4a
0x407180:       0x1e0f5a1d0b1618f6      0x6d30b9cb90f9783a
0x407190:       0x5c0d282d5c31d9c6      0x78a2ecab80a94a7f


no idea how to get the pattern for this, maybe there is a way to brute force instead?
new idea, look at where it writes to the memory and then figure out how the writing occurs in the disassembly 

1 
0x407120:       0x2c6d1a1a4b06ebc6      0x6a118bd9a7cb7878
0x407130:       0x2c6d1a1a4b066a47      0x6a908bd9a74a7878
0x407140:       0xad6d9b1a4b06ebc6      0x6a110ad9a7cb7878
0x407150:       0x2c6d1a1a4b06ebc6      0x6a908bd9a7cb7878

2
0x407120:       0x2c6d1a1a4b06ebc6      0x6aa08bd9a7cb7878 <-- diff at second byte
0x407130:       0x2c6d1a1a4b06dbf6      0x6a908bd9a7fb7878 <-- last byte
0x407140:       0x1c6d2a1a4b06ebc6      0x6aa0bbd9a7cb7878
0x407150:       0x2c6d1a1a4b06ebc6      0x6a908bd9a7cb7878

how to detect where they moved?



maybe the buffer also contains some of the reads and writes?
could be that the buffer we submit is also a sequence of opcodes
how to operate on these opcodes?
for each opcode, a
could be that we're providing the data for the machine which is doing something?


maybe i should write some code to simulate the machine?
need to read in the bytes, but then what

0x19 -> 0x7a isn't bad?


also, we only get the first 8 bytes in memcmp, so there are more operations later on
probably good to build a machine to emulate the instructions

0000000000405080 -> 4058d4
0x00203a7475706e49       <-- there's also this initial value

# TODO:
1) some of the values are two large in my_buf
2) not sure how the vm implements the wrap-around
3) something is wrong with the buf modification code as well
fk this virtual machine 


i guess could also try to keep track of whenever the scratch buffer gets written to???
also, need to fix the buffer overwrite, not sure how that is handled in the actual code
maybe set breakpoint when the value becomes something in gdb to handle instead


okay, let's keep track of each time a byte is written into a position in my_buf
in memory modification from other places
develop hook fn for specific value to just drop

ok first, what is @property in python?
what is the order of init in python?

looks like it takes the entire row and modifies it 
so keep track of 
1) reverse the bit value 
okay, it could be copying a value from a memory position as well as opposed to doing xor stuff, i.e. our initial input gives us the new value 

find which input gives us e2 
but it's also possible that it takes multiple inputs in order to get e2 so changing a single value might not be enough

okay, the scratch buffer is moving values 
let's see where it gets the good values ig?
we need to find the positions it is using

okay, we have the array of numbers we are drawing from 
now how does each byte get those true positions?
if we were just grabbing from a position with our input, the 0's would have given us the same value but it didnt so we must be using something else
but what?
each input value gets moved somewhere else, then how does that moved value get the new value?
input -> reverse value -> random position -> ???
oh yea offset + i 
ok so it's from the pos value, so how were those values modified is the question
but how can those positions be the wrong value
ok at what point is the self.state modified?
ok the state looks like it never got modified?

is it just an xor
idk why i thought this was so hard but i see the xor key now and the user input


bit flip final op?

reverse -> xor -> then what
key chunks 
1) key chunks ^ with flipped user input
2) 


it writes AFTER doing the memcmp so the memcmp return value should still be stored somewhere so our hypothesis should still be correct i think 
something got remapped clearly

at this op we can draw out the values maybe 667


pos 0 gets flipped
pos 0 mapped to pos 17
pos 17 gets xored with key
do check on flag

xor key with the flag 
now, pos 17 values SHOULD be in pos 0 so move them there
then reverse the values


