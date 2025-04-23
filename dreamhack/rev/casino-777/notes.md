most likely we need to call the spin function multiple times first?

what is the initial config code doing?
what is the triple deref doing?


generate_config function:
    for i from 1 -> 10 
        call malloc of 16 bytes and assign to an array
        malloc stores some character + 1
        get a random character, and if the character i '7', then set a flag.
        if the flag does not get set, then the last character will be 7

then rotate_slot does something 


ok so we have some initial slot layout from /dev/urandom
and these values are stored in memory at 
will i have to use a solver for this??? not sure


in gdb, the first address is 0x00005555555592a0 
so using the slots, we need to find out where each 7 is basically 
i also want to double check where the memcpy is happeningj

0x555555555796

okay, something is being overwritten but im not sure what exactly
this reminds me of chinese remainder theorem 
like figure out position of character, and rotate all of them correctly essentially 
but let's see


first memcpy:
dst = 0x7fffffffdbb0  <-- dst, stack 
src = 0x5555555592c0  <-- heap
src contents is rotated version of dst contents

before
*RDI  0x5555555594e0 ◂— '8KmAoG7umtjWYGR[<"~q@84[Qc\\;.V++G17@83rOSAG@{O4Ty)dOv3r~1+Nj9@VS>92|IJ
3>F7Ft5mq8#?%j\\.suGzBRm5qi-9@P!,['
 RSI  0x7fffffffdbb0 ◂— '++G17@83rOSAG@{O4Ty)dOv3r~1+Nj9@VS>92|IJ3>F7Ft5mq8#?%j\\.suGzBRm5qi-9@P
!,[8KmAoG7umtjWYGR[<"~q@84[Qc\\;.V'

after: 
 RDI  0x5555555594e0 ◂— '++G17@83rOSAG@{O4Ty)dOv3r~1+Nj9@VS>92|IJ3>F7Ft5mq8#?%j\\.suGzBRm5qi-9@P
!,[8KmAoG7umtjWYGR[<"~q@84[Qc\\;.V'
 RSI  0x7fffffffdbb0 ◂— '++G17@83rOSAG@{O4Ty)dOv3r~1+Nj9@VS>92|IJ3>F7Ft5mq8#?%j\\.suGzBRm5qi-9@P
!,[8KmAoG7umtjWYGR[<"~q@84[Qc\\;.V'


okay we can leek the location of each 7 pretty easily i think since it does a mod
yea im pretty sure this is the solution

yKd:zdAn\
!76b1@$sL
hz+he}

when we submit rotation = 0 -> should be nth character of each 
only get 1 byte of rotations???
yea still should be fine, but not sure why i am crashing out before finding all the 7's

i think we might be overwriting some data on the stack from the memcpy possibly 

okay, not all of the 7's are getting printed


yea some position has a 7, but not all of them could def be that something is getting overwritten

W A J & @ Y 5 e B r 

. , - I ) M & 1 Z z


okay, it's actually rotating backwards?
so it goes from the last character

okay, got them all out 

1) get all the positions
2) because they start from backward, calculate from the prev position
abcde  -> eabcd -> deabc


so the real position should be (sz + 1) - pos, assuming sz does not account for the malloc + 1?
this gives us the real position

0x48
0x52
0x58
0x60
0x66
0x4e
0x64
0x7e
0x82
0x88

j9Dj\\ghA$2~!f\"Ql{{srtW=EoutlyPD|yv0=faC0or\"SDr[ARPa1jQCH<m}S]JT~&uK1E7D%W"

so when we see 7, we should store it as 4
then we keep going until all the 7 characters are identified / locations are found
this leaves us with \[new amount\]\[7\]\[rest of characters\]
| new amount | 7 | rest of characters |
so we need to find the number that rotates 7 back to the beginning
need to rotate by the (rest of characters + 1)
so we need to keep track of new_amount as well after the last character
for each loop, we need to keep track of the front difference


okay... it changes because the new 



a e d c b a e d c b ... 
there is a max value that we have to keep rotating until we find the characters we want

- max number of rotations - padding until next 7 -  

- maybe easier to just keep track 
rotated incorrectly, so need to find offset to the next 7 from current pos 

i think when number gets too big it cannot rotate cuz it's a C program




