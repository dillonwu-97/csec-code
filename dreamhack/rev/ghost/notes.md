is there an sbox used in this problem?

taking a look at how the loop gets updated

cmp rcx, rbx <-- go up to 60 
rcx = j 
rbx = max val 



loop checks if any characters are pass the ascii readable range, and then does something if it is but not sure what that is

comparing r12 and r10 registers but to what end?
r12 is being pulled from the data section?? not exactly sure merp 
is it trying to match values from the data section?
0xc000137338 <-- sbox looks like it contains important values? from the sbox potentially?
maybe we are passing in indices that are being used for a search

cuz the value returned is alwasy 0x152a

these are the values passed in as well
*RAX  0x152a
*RBX  0x36
*RCX  0x80
*RDX  0x36
 RDI  0xff
 RSI  0x37
 R8   0x75
*R9   0x7f
 R10  0x37
 R11  0x75

these args are passed into the segment tree but im not sure to what end 

okay, first check is for length; needs to be 60 characters
then, only do something if the value is >= 0x80

could just be checking that the input is ascii printable 

the non-ascii characters might be expanded? not sure but it counts incorrectly if it's not ascii 

bdbfef <-- new value from our original value; how it get here tho
always bdbfef if greater than 0x80 i guess?

okay, we actually failed out?? huh 0xfffd in rax for some reason

seems like we crash out, but im not entirely sure why it happens 
break at the assignment instead and see what happens
okay the forward implementation looks correct

                         0x48e0f7 
i guess this is part of the problem??
maybe i have to provide runes / special characters that i'm missing?

yea i think i might be missing the go runes part of the problem 

what does decoderune do?
but even if get the correct byte, it feels like im still stuck because i cant find the next byte character in the sequence??
probs need to submit utf-8 valid string and it gets decoded correctly i think 

i think i should take a look at how runes are constructed because it might be xoring with the character i think it is xoring 

# 5/29
Okay, i forget where i paused in this problem  
I think i was having trouble passing in as input the correct character
the problem i was encountering (even though I think my algorithm should be correct) is that it is failing after a specific character and also i cannot find a subsequent character after a certain point  
this doesnt make any sense if the algorithm is correct, which it should be because it works for the first few values in the array so like what the fuck 
does something in decoderune modify what i need maybe??? idk merp



--> Merge from another notes file, so somewhat scrambled


0xc000128050 <-- contains some values, but not sure how they were generated

0xd2, 0xf3 from the sbox so not necessarily right i think 

not sure why it is called sbox?? very confusing hmmm 

this is the sbox, it looks kind of like 
but it doesnt match up with the actual sbox 
0x7e
0xc00011f870:   0x0000000000000080      0x00000000000000ba
0xc00011f880:   0x000000000000007d      0x000000000000006b
0xc00011f890:   0x00000000000000be      0x00000000000000c4
0xc00011f8a0:   0x0000000000000061      0x0000000000000092
0xc00011f8b0:   0x00000000000000c9      0x0000000000000049
0xc00011f8c0:   0x000000000000004c      0x00000000000000a0
0xc00011f8d0:   0x0000000000000096      0x000000000000003a
0xc00011f8e0:   0x000000000000009e      0x0000000000000048
0xc00011f8f0:   0x00000000000000e7      0x000000000000005f

0xc00011f870:   0x0000000000000080      0x00000000000000ba
0xc00011f880:   0x000000000000007d      0x000000000000006b
0xc00011f890:   0x00000000000000be      0x00000000000000c4
0xc00011f8a0:   0x0000000000000061      0x0000000000000092
0xc00011f8b0:   0x00000000000000c9      0x0000000000000049
0xc00011f8c0:   0x000000000000004c      0x00000000000000a0

okay, the values look the same but how is it initialized in memory?

0x7f are better i think 
random seed function thing is used?
cant tell how the random numbers are generated
this better not be another shitty sbox problem 
what is old array?
what is 0x71e8 tho

okay, what ideas do we have so far?
we have some sbox that contains values shared across instances of the program
there is an add value and xor value that gets constructed as well
we could also be updating the sequential arary at some point

Questions:
1) what are segment trees?
maybe let's just see what the before and after of the tree is; might be better
this is kinda hard; idk what is being updated
am i just reversing the stupid ass segment tree
okay, i think my intuition is telling me that we have to submit some input which is a segment tree
then we make queries for xor and add and they have to match up? maybe something like this idk 

at 0x48e13a, the position is 0x7e and the value is 0xf1
yea, we pass in positions as input up to 0x80 

0xc000128000 <-- storing the new orientation
11      breakpoint     keep y   0x000000000048e14d in main.do_sbox at /home/leesu0605/go/bin/prob.go:19
        breakpoint already hit 1 time
12      breakpoint     keep y   0x000000000048e0e9 in main.do_sbox at /home/leesu0605/go/bin/prob.go:18
        breakpoint already hit 1 time
13      breakpoint     keep y   0x000000000048e0dd in main.do_sbox at /home/leesu0605/go/bin/prob.go:19
        breakpoint already hit 1 time
breakpoints for what i was looking at
^-- this is the first loop

let's see what the second loop is doing
grabbing the sbox value it looks like and saves it as an "add" value
when did r9 get modified???
so is there maybe a second swap happening??


part 2 pseudocode:
something like this maybe:
1) new_store[0]
new_store[1]

if new_store_sec > first, swap


1) where are 0x37 and 0x75 from again? how to get them from 0x41, i.e.
i think it's sbox[0x41] = 0x37? <-- idk, need to double chec
but then where is 0x75 coming from
0xc000128000 <-- stores the new values, should be 0x37 all if theory is correct
ok yes, the theory holds up, but where is 0x75 coming from then 
0x75 comes inside of the second loop, and it takes the value from the position 0x37, so it's a two layer indirection 
so it compares the first level indirection value with the second level indirection value and if the second value is less, swaps them?
    <-- no not exactly, so it's more like  
        a = arr[0]
        b = arr[a]
        c = a[1]
        then compare b and c, if c >= b: swap 
2) how is the segment tree used?

3) is the array being expanded / why is it being expanded
yea nt sure if i need to worry about growslice tbh

4) - [ ] Add variation to the input payload so i can see what is happening 

0xc00012e000:   0x000000000000152a      0x0000000000000036
<-- how are these values calculated?

okay, the memory in go moves after the array gets resized 
also, at each breakpoint, 0x36 gets written to the right and 152a gets written to the left 

0xc0001ba080:   0x00000000000005ef      0x0000000000000007
0xc0001ba090:   0x00000000000014fa      0x0000000000000006
0xc0001ba0a0:   0x00000000000014fa      0x0000000000000006
0xc0001ba0b0:   0x00000000000014fa      0x0000000000000006

hmmm many changes, 
what is the left / right values? need to know this as well 

# 5/19
Okay, what are the right and left values 
the value changes depending on what value i submit to the payload 
Need to know  a = b
1) what comparison is being used, i.e. what b is
2) how a is generated based on user input

it says segment tree, so it takes some range and adds or xors it presumably 
input array -> transformation -> new store I think 

sequential_arr start addr: 
0xc000127980 <-- might not be static fml 

pwndbg> p 'runtime.buildVersion'
$1 = 0x4c6f60 "go1.18.1"
Question: How does go handle the differences in ABI of a go binary

void __golang segment_tree_query(main_info_0 (*seg)[1500], int nd, int ns, int ne, int qs, int qe, main_info_0 _r0)
{
what is each of these?

main_info seg 
nd 
ns 
ne 
qs
qe 
main_info r0?

ok, so each of the left / right thingies are used to store the left/right segment object 
- [ ] Understand how the segment tree thing is implemented
- [ ] Understand what segment_tree_query is doing b/c it no look like query

what is second / first though?
it is the sbox from user input
then there is another layer of indirection based on the first value 
so if 0x41, 0x43
0x41 -> 0x37 -> 0x75
looks like it is building the segment tree and it's doing addition 
ohhhh interesting; it looks like it's doing a store of both rax and rbx, where rax is the addition return value and rbx is the xor return value 

okay, now what is update_seg doing? 
yea looks like an update, but update with what 
there is also some level of ordering that is applied
are those memory values nodes?? hrmmm 
might be get seg, not update seg actually 
not an exact xor so maybe there is something that is done to the segment tree ops 
in the update section maybe
but also b/t which values is the xor / addition happening?
we have the correct values in memory as well
i need to verify where the original segment tree is / the values in the tree 
triple xor?? or something?? seems like we have an off by 1 for most of them?
e.g. 0x75 ^ 0x94


0x75 ^ 0x94 = 0xe1
0xe1 ^ 0x37 = 0xd6
0xd6 ^ 0x89 <-- this is the double deref for 0x43 = 0x36
so it looks kind of similar?
0xc00014a000:   0x0000000000001090      0x00000000000000e0
0xc00014a010:   0x0000000000001f3f      0x00000000000000d7
0xc00014a020:   0x000000000000103e      0x000000000000005e
0xc00014a030:   0x0000000000001f20      0x0000000000000036
0xc00014a040:   0x0000000000001090      0x00000000000000e0
0xc00014a050:   0x0000000000001f3f      0x00000000000000d7

okay, so not sure why we have a +/- off by one error 
yea specifically 0x53 and 0x36; where are these from?


or it could be that one of the values specifies a range as well, this is also possible merp 
in theory, what might be happening is idx[0x37] ^ idx[ idx[0x37] ] ^ idx[0x37] ^ 0x1? <-- maybe but that doesnt make sense 

looks like it's always the two adjacent values that we submit 
0xc000156100:   0x00000000000005ef      0x0000000000000007 <-- but how is this value constructed?
0xc000156110:   0x0000000000001af7      0x0000000000000001
could be from the update segment part of the code?
not sure what the update is doing, but should check it 
ohhh wait, it must be prev and current 
so rolls from 0x41, 0x42 at iter=0
    -> 0x42, 0x41 at iter=1; yea positive this is it 
    then back 

okay, now how to formulate the addition step?
could bean addition between the numbers
yea im pretty sure this is the solution
okay, let's do an addition between the values 0 -> 0x75?
but then why are the values different
is it adding the sbox values? what is being added / being constructed?
it must be the difference, okay maybe not actually
but it swaps the value 
but wat is the running sum?
/ what is the range requested?
where is 0x69 coming from tho 

maybe just the lower layer / branch for the segment tree?, i.e. each immediately adjacent value
okay, this is my current running theory i think 
okay, i think my xor algorithm / implementation is totally off but im not sure why 

okay, retrying the thing i looked at:

okay, i'm off for every other value 
will take a look at this tomorrow i think 
was it a double deref each time?
oh wait i think there's also a swap, so maybe it always uses the smaller value first?


# 5/20
Okay, it actually looks like the value in the sequential arr changes
but where does it get modified?
Looks like it gets swapped around but not sure y 
update_seg modifies the value but not sure to what end
i should try to note down what value gets stored 

# 5/21
Okay, goal is to finish this 
there is the sequential_arr that gets modified so we need to take a look at that 
sequential_array is not always sequential; it will contain swap values at a certain point 
seq_arr is actually swap_arr
then, take the value and xor and save it i.g.
and then do double deref on the swapped value which is why there is probably some sort of triple deref thingie at some point
like, at the deepest recursive layer, i am not sure what is rax rbx. it should be some leaf value but what is the tree? 
is it the array that we submit?
if it's just the immediate values, that wouldnt make any sense because then we wouldnt have any need for the segment tree so how is that used? and where are the input values used to construct the tree even located?
the segment tree looks like the sub/seq array i think 
i dont understand what values are being used and why the leaf case is not being hit more often
it looks like we are hitting the non-leaf case 3x more than leaf case, so did i get the two swapped maybe???

rdi = upper bound i think 
0x37 = search value?
kinda close actually; would not be surprised, and then the xor value could be in that range as well 

build_seg_tree adds the range of values but im not sure why xor doesnt xor the range of values
it looks more like it just xors the previous element
yes it is xoring the range of values
then update segment is doing a swap of some sort  
okay yea im close to solving this problem i think 
update happens twice, but why
okay, two different swaps 
first update_seg does the following swap:
larger_val(?) <-> seq/sub_arr_first pos
second update_seg does the following swap:
smaller_val(?) <>-> seq_arr [ second pos ]
example: 
okay i need an example, because i question the validity of the previous statement actually 
firs val = 0x01, second = 0x02
deref_0x02 0x01 are swapped 
and 
deref_0x01 0x02 are swapped


dam i dont know if i want to implement this right now
- [ ] Grab the values from memory
- [ ] Brute force sweep to the right (larger numbers)
- [ ] Bruce force sweep to the left (smaller numbers)

i need to retry with a test case that works / i know for certain
- [ ] Create own test case with "acdef" values
- [ ] 


is there something i did wrong with the swap?? idernt knaur 

Okay, the sbox looks correct, i.e. the sbox looks fine 
So what am i missing?
do i need to make multiple updates or something?
is that even possible atm??? 
are there multiple candidates for something??
