length is 48
looks like another segment tree
not sure if the update mechanism is the same though; probs not, otherwise it would be the same problem as before


yea main_update_seg looks different
not sure what it is doing now though 


- [x] Grab the sbox again
- [ ] Rename the variables in the code so that it is more clear what I'm looking at
- [x] Figure out what needs to be satisfied by looking at the output we need
    - [x] i see some values  but what is the iter count?
- [ ] Figure out what the update_segment part of the code is doing
     - [ ] there are a lot of values that are being modified 
     - [ ] what is the diff between arr and seg values?
     - [ ] what is the math in the update seg section trying to do?



0x52ada0:       0x000000000000864f      0x000000000000058b
0x52adb0:       0x000000006e07c908      0x0000000000009222
0x52adc0:       0x0000000000017fc6      0x0000000000007826
0x52add0:       0x0000000008165600      0x0000000000008ac8
0x52ade0:       0x000000000002087d      0x000000000000c11f
0x52adf0:       0x000000003663a00c      0x000000000000b4ff
0x52ae00:       0x0000000000030fec      0x000000000000318c
0x52ae10:       0x00000000f9d90000      0x000000000000000c
0x52ae20:       0x000000000004cb1c      0x0000000000009032
0x52ae30:       0x00000000826fb410      0x000000000000ed89
0x52ae40:       0x000000000006c156      0x000000000001f2ae
0x52ae50:       0x000000004d753900      0x0000000000004486
0x52ae60:       0x000000000004cf89      0x000000000002b183
0x52ae70:       0x000000002b8636d4      0x000000000000f7c7
0x52ae80:       0x000000000003b2e8      0x0000000000038d08
0x52ae90:       0x00000000f0040000      0x0000000000000800
0x52aea0:       0x000000000003f2b5      0x0000000000031c49
0x52aeb0:       0x00000000409a3700      0x00000000000003c6
0x52aec0:       0x000000000007bc3c      0x0000000000002b80
0x52aed0:       0x00000000f0648100      0x0000000000006c0a
0x52aee0:       0x000000000005e4ad      0x0000000000003db5
0x52aef0:       0x000000003df0a6e8      0x0000000000002eb2
0x52af00:       0x0000000000004b9c      0x00000000000033e4

okay, in this hex tray, which values correspond to what? 
yea, just have to figure out how to calculate each of the individual values 


there were add_vals / xor_vals in the previous problem; 
at tis address, h0x48db60, we can see that there might be such values used once again
oh but they're changed in intervals
looks like there could be another swap array as well

0x48df88 <main.main+168>    lea    rax, [rsp + 0x1098]     RAX => 0xc000141058 ◂— 0
   0x48df90 <main.main+176>    lea    rbx, [rsp + 0x898]      RBX => 0xc000140858 ◂— 0

first one is segment tree, aka at 0xc000141058
second one is the swap array, aka at 0xc000140858 


0xc0001b8020  <-- looks like scratch buffer to store the new values we want to write or something

0x52ada0:       0x000000000000864f      0x000000000000058b
0x52adb0:       0x000000006e07c908      0x0000000000009222
in each 2x2 block, which matches which operation?
at idx 0, this is addition
idx 1 is xor
idx 2 is mult with another mult value in the same pos (by which one?!)
idx 3 is get the last byte, and then OR with the mult value again, from the same pos


000000000048E12D <-- this instruction uses the sbox 
how is the new array from the sbox used?
the memory also looks like it's being frequently reused which is pretty annoying 
is the sbox being modified at any point in time?


there is another array that gets used somewhere that is increments of 3
found at this instruction: 0x48e475 <-- not sure how this is used / where it comes from though 


okay, revisiting the goal for this problem
we just need to find out how each value is constructed
so let's 
- [ ] find out where the array will be at a given run
- [ ] set a watchpoint to see when that value is modified
- [ ] step back to see what was done to modify that value
- [ ] repeat for each of the other 3 squares

Need to identify where the first write will happen, and then set a breakpoint on the next iteration
man in the middle to trap Crowdstrike alerts from coding could be possible



# 6/2
0x48e15d <main.main+637>    xor    qword ptr [rbx + rdx + 8], rax        [0xc000150068] => 0x1810 (0x0 ^ 0x1810)
rax looks like it is gathered from the build_segment_tree return value
first value is 0x604 <- but how derived?
again, where is the base case return value and all that fun stuff?

0x1f0, then 278, 0x19c and then we return back to the original call
0x1f0 <-- 9th pos
0x278 <-- +9 from 8th pos
0x19c <-- 
0x1f0 ^ 0x278 = 0x388
Not sure how the original values are derived, but if it's building a segment tree then it probably comes from xor of input values or something

rax at some point returns 0x37 so wtf is up with that
and 0x3e0 <-- not sure where this comes from either 

0x4f0 
338
0x6e, 0x6e, 0x6e

0x5d0, 0x768, 0x4d4

0xa5, 0xa5, 0xa5

0x7c0, 0x9e0, 0x670

Different values depending on input array (obv)
is it storing all of the segment tree values onto the stack?
hrmm not sure 

maybe one of the first boxes takes the sum of some values; but how are "these values" derived? how is it related to the sbox?

# 6/3
- initial segment tree looks like addition segment tree
- looks like the update tree code is just building the tree with just addition operations

address at first:
0xc000142020
okay, i need to identify where the values are stored

build_segment_tree returns the value for 0x604 <-- how this value used though?
if build_segment_tree is the sum of something then shirley, 0x604 is the sum of some values
let's see when it gets returned in the segment tree code
this is calculating the first box i suppose
iht is 0x414 + 0x1f0 
where do these two values come from?
0x19c <-- where this from?, is it 0x37 position value in the segment tree?
how is the initial segment tree generated?
0x19c + 0x278 = 0x414
0x414 + 0x1f0 = 0x604
how are 0x19c, 0x278, 0x1f0 generated
value diff depending on the input
what values are used to construct the initial values of the segment tree? why would construction be different based on initial input?
i think update_seg comes first, and then build_segment_tree does the iterative addition
so we should start by figuring out how update_seg constructs the initial values and where these values are written in memory
we are not hitting the negative branch for some reason

- [ ] Let's see what the segment array value is before and after the div calculation is done
- [ ] say with the substitution array 

# 6/6
0xc000123858 

0xc000122858

these are two different arrays, but how are they diff in terms of memory?
also, why are there two different ones?
increments by 2, then 3, then presumably all the way up to n?
yea, it divides and then multiplies 
but how is the tree used at each iteration
how many times does the outer loop ctr run? thought it was 256 but maybe not
oh actually i think it's only 48 times
- [ ] Check final values at last iter
but the gap also doesnt look like it is 0x30 so what is up with that 
0x30 -> 
build segment tree then constructs the value

is there anything being swapped?
the diff between each value is also not 0x30 so....
at 0x20, it is 0x9 difference instead of 0x20 which is not what i expect

at 0x09, then diff b/t values is 0x03
why values not being modified wtf 
update_segment works on which arrays 
let's see if the segment tree gets updated at each iteration or if it's updated at every 4 iterations

7f80
7f81 
looks like it's adding 1->12? yes, but why.......
because going through 256 times?
not sure how the seq array interacts with the solution array that we are constructing
1       breakpoint     keep n   0x000000000048e23e in main.main at /home/leesu0605/go/bin/prob.go:106
15      breakpoint     keep n   0x000000000048db60 in main.update_seg at /home/leesu0605/go/bin/prob.go:46
16      breakpoint     keep n   0x000000000048e484 in main.main at /home/leesu0605/go/bin/prob.go:109
17      breakpoint     keep n   0x000000000048dbde in main.update_seg at /home/leesu0605/go/bin/prob.go:50
18      breakpoint     keep y   0x000000000048dbe3 in main.update_seg at /home/leesu0605/go/bin/prob.go:50
19      breakpoint     keep n   0x000000000048dbf9 in main.update_seg at /home/leesu0605/go/bin/prob.go:50
20      breakpoint     keep n   0x000000000048dc17 in main.update_seg at /home/leesu0605/go/bin/prob.go:51
22      breakpoint     keep n   0x000000000048e4c9 in main.main at /home/leesu0605/go/bin/prob.go:108
24      breakpoint     keep y   0x000000000048e1c4 in main.main at /home/leesu0605/go/bin/prob.go:104
        breakpoint already hit 5 times
27      breakpoint     keep y   0x000000000048e264 in main.main at /home/leesu0605/go/bin/prob.go:107
        breakpoint already hit 2 times
28      breakpoint     keep y   0x000000000048e484 in main.main at /home/leesu0605/go/bin/prob.go:109
        breakpoint already hit 29 times


i have the pattern used for constructing the tree, now i have to figure out how the individual values are constructed
0x7f80 -> something else, thought it was reevaluating the new tree after updating from 2->3->4 increments, etc. but maybe that's not the case
update segment is doubling the value which is what we expect, then triple
okay this makes some sense
the segment tree is getting double, trip, 4x, etc. up to 12 x i think  
and each chunk should be the sum between a certain range
the next step is to understand how the four chunks are constructed
what is the modifierl_val? 
right 0x604 <-- how constructed?
(0x37 * 0x38) // 2 = 0x604 so it's the sum 
and 
(255 * 256) // 2 = 0x7f80 so that's another thing we have

is there any swapping crap that happens again?
3rd cell starts with value = 1
i think all i have left to do is to figure out how the sbox is used and i should have a pretty solid idea of how the values are constructed

but sometimes, just 0x37 is used so that's kind of weird 

modifier val = sum of something
first cell: sum of a range of values and current 
second cell: xor of what and 
maybe when build seg tree doesnt run / isn't updated, the default val is returned? not sure
maybe if i solidify the addition operation, i can get the rest
when not mod 4, just get the regular value i think, but how those derived?

looks like 0x6e comes from 0x37 * 2
then 0x37, 0x6e, 0xa5 so 0x37 gets added to the prev
need to check if it's just an incremental addition at each interval 
probs not because we get the value back from the segment tree
lets do 4 diff values for each set up to 12 sets

0x94 * 2 = 0x128
so the general idea is 
for each 4th value, the array gets updated
the next val might be a range
so the modifier val is a range
need to check if the modifier val is somehow appended to previous values somewhere
at each interval, how do the values build on top of each other is the question

0x604 + 0x2545 + 0x1e6a + 0x762

then reset

- [ ] Get the additions working

okay, i think i have the solve
but idk how to do it fast unfortunately 
0x9222 <-- so each of the values ends in 2?
first one is 0x9
fawkin algorithms problem
hashmap something something 
ok the algorithm is: 
for each sum starting from 0 that ends in the higher byte nibble, save that value
    for each value start from each of those, find the values that give the next nibble
        do that again
            do that again 
            so we have a tuple of 4 values now (a,b,c,d)
            get the sum / product / xor_val of each to see which one is correct



after getting the values, need to get their corresponding index to get the original value i think 


# 6/10
i think i am missing something else, but sbox substitution stuff
but that should come after
there is a weird off by 1 error that i need to fix 
i am not sure what to do here
i feel like the math is correct but maybe an array gets updated or something like that and i missed it 
hrmmmm 
this is taking a long time, but it's found


 [72, [0, 81, 43, 174, 43], [0, 183, 102, 102, 226], [0, 142, 42, 180, 226], [0, 71, 64, 223, 42], [0, 227, 183, 89, 1
93], [0, 227, 64, 183, 227], [0, 241, 241, 199, 227]]

DH{H3ll0!_G0hst_r3vers3r~~Or..M4sTer_0f_z3?!_;)}

# very slow, atm but i dont want to optimize the code
but i might have to do a rewrite zzz 




