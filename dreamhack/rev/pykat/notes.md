need to use python decompiler again i think 
okay, how to get the python code from the bytecode now, it is throwing some error that i need to figure out
- [ ] read through the error and try to dump out the backdoor code correctly

decompyle3 worked kinda ok

POP_BLOCK instruction failed
pycdc didnt work as well as decompyle3 actually lol 
maybe i can write my own janky decompiler?? actually that might be too hard, but getting the assembly without the decomp would be doable i think
okay, when have time:
- [x] Try to get the bytecode dump, not the full decomp


# Notes
- Looks like stream 29 has an encrypted binary
- also a result.txt file
- so the backdoor sends files and also shows the files in the directory; so first the atker listed the dir and then it tries to grab SS.exe and result.txt
- probs need to grab the key from the wireshark capture, decode the result and exe file to find what we want
what the padding ? Crypto.Util.Padding I think; let's try with result.txt
- okay, how to reconcile result.txt and the extracted binary? 

Navigate to _ZNSo5writeEPKci

Press Y to open the type declaration editor

Paste this (if you're sure of the prototype):

std::ostream *__cdecl _ZNSo5writeEPKci(const char *, int);
That allows the decompiler to parse arguments and return type properly.
<-- replacing that with this fixed the decomp but i have no idea why


/* Orphan comments:
what is this writing, there is nothing in that region in memory
*/
    <-- found this comment in the disassembly so maybe i need to do the disassembly dynamically or something i dernt kner

okay, i think i will definitely need to do this dynamically
statically will be quite hard to pin down the precise details
okay, i think i need to enable the internet and install mingw++ compiler and i will get my libraries


00007FF7818B1000 | 48:895C24 08             | mov qword ptr ss:[rsp+8],rbx            |
0x007FF7818B2000 


okay, we are missing a dll
let's see if the dll is in the other binary
e.g. if it is maybe we can dump out the memory or something?
okay it's not here hrmmmm

dependency walker is not working either for some reason

okay, i am not sure how to get the executable to run 
i know that it was compiled with 
maybe i have to run on the mingw terminal <-- this is another possibility, and then i just attach x64dbg process or something like that?

i wonder if this is related to exception handling?
the library that we are missing which prevents us from reversing dynamically is libgcc_s_dw2-1.dll which is a dll for the dwarf-2 exception handler. This is in contrast to other exception handler ABI's like Window's structured exception handling.
These are some interesting reads I think
https://stackoverflow.com/questions/15670169/what-is-difference-between-sjlj-vs-dwarf-vs-seh
https://gcc.gnu.org/legacy-ml/gcc/2002-07/msg00391.html
https://sourceforge.net/projects/mingw/files/ <-- found this from this github post
https://github.com/Perl/perl5/issues/18510
ok, now im not sure what it is im downloading tbh from prdownloads.sourceforge
okay, yay it runs after grabbing the files from the link above ^^^
okay, i go into the exception handler immediately at address 6eb562b1 which is in the dw2 dll file 
interesting that there is some tls callback code inside of the executable itself
in theory, if there is nothing overlapping, then we should be good so let's just try and see, i expect there to be DH{ at the beginning as well, i.e. each part of the result file gives us a chunk of the flag 
let's just get a test string to see if it works 
okay, also id_val is the first few characters, not the complete set


                                                

ID: 
2CPGAnU4%FO5HB6VT09m3 
bbbbbbbbbbbbbbbbbbbbb
length = 21


Password:
8e16e5b2c446aea3b142d9320755f82932fc2cdf
aaaaccccddddeeeeaaaaccccddddeeeeaaaacccc
length = 40

need to figure how result.txt is being written to 
404b28 looks like it takes in the first four characters of password?
yes, but not sure what it's gonna do with these characters 
okay, i think the write is not to stdout but to the result.txt fd 
i think esp+4 contains our input 
at esp+4, first 4 bytes is the constructor, length, and then the actual data i believe
interestingly, i dont see AAAA in memory when I pass in AAAABBBBCCCCDDDD as input for some reason


looks like the input id is specifying the position to search for in the string
0123456789ABCDEF  
GHIJKLMNOPQRSTUV  
WXYZabcdefghijkl  
mnopqrstuvwxyz!#  
$%&()*+-;<=>?@^_  
`{|}~
0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!#$%&()*+-;<=>?@^_`{|}~
which is also of length 0x55

yea the id_val constructs a new string using positions specified by id_val and stores it in a place in memory 

could be that it is calculating sha1 values in smalll incremental chunks so we could be tasked with brute forcing some of these values potentially 
at some point, the data gets consumed 

-> always generates 41 characters
-> 40 -> 42 character blocks 
so not always 42 for some reason; not sure why that's the case
-> 5 blocks of hex 
-> 10 different blocks 

# 6/24
- strangely, nothing got written out of the program, was expecting result.txt file so not sure what's going on there
- yea, not sure why something didnt get written very strange 
- not sure what the chunk after the password / before the next hash is? 
actually i see it 
for the input 
aaaaccccaaaaccccaaaaccccaaaaccccaaaacccc <-- 8 * 5 = 40 = 0x28
there is a repeated pattern of the following after the id:
1) hash of first 4 chars
2) hash of first 4 chars ^ hash of next 4 chars
3) hash of next 4 and prev
...
11) hash of next 4 and prev 

H(a), H(a) ^ H(c), H(c), 0, H(a)
okay so i can recover the original password but what is the mersenne thing?
also, how is the id_val used / do we need to reverse that completely?
might be close to solving this one

wtf is the mersenne twister used for then???

# TODO:
What I think we need to do so far
- [ ] Extract the values generated by the mersenne twister and reverse that to recover the input values maybe?
- [ ] Alg to check that the sha1hash helps us recover the original 4 characters
- [ ] byte by byte xor 
- [ ] The what's up input is 4 characters long and constructed using mersenne
    <-- we might be able to brute force this
- [x] code to recover the original ID
    --> idea is that the input string provides a position
    --> position gives us a char in another string
    --> for i in range 0 -> 21 swap arr[i] and arr[char_at_pos]
        <-- how reverse this?
        <-- wtf how do i reverse this
        <-- okay, need to think more about how to reverse this tbh 
        <-- okay i guess the user input is much shorter though
        <-- also not sure how the original character is represented; that's another thing, okay it gets the order of the character and takes it mod 85 meaning we in fact can get index 0 
        <-- probs something like wane_is_administrator


id: 
Wane_1s_Adm1f1strnt0r
aaaaccccddddeeeeaaaaccccddddeeeeaaaacccc

one character is off 
2CPGAnU4$FO5HB6VT09m3 <-- ok fixed
2CPGAnU4%FO5HB6VT09m3

# 7/18
long time since i looked at this 
okay, what was the goal again?
provide some user input that matches our output i think 
fuck, did i not write down the input that works???
okay, i think that id works but maybe we need to verify?
looks ok though 

now, need to calculate the next chunk, i.e. correctly get to password
okay, let's write the code first for getting the password

ok, not sure what the chunks are though 
what is the has that gets written afterwards?
it's not the id and it's not the password input

split by 0xff is te move 
there is also a mismatch between the number of 0xff in result vs the number of 0xff in the actual payload 
the length for each hash is also different which is very weird
hash starts from the second chunk actually so that's something else to know 
very confused about why there are more characters in the second val than 80

First four characters is "Real"
Found!
Real <-- from output

but is the next chunk not the size of a sha1hash?
second:

# used a rainbow table because faster
Real
Secu
rePa
sswo
rdlo
l

password: 

6ff44ddab66a9543aa2390df052cbe5b9a446460 Secu
71f5b2dd95021a87a4e7b2b8919161d25aafcdfb rePa
a7fa36dcef025ee4f9b3f83aff8f8216285b663d sswo
a49a1ef1724bd2481766f97d70e20d1e812690b1 rdlo
07c342be6e560e7f43842e2e21b70d961d85f047 l




okay, this was kind of guessy but I got rid of the 32nd character and it worked 
the problem is that idk how the character snuck in there

one idea is that it uses the password as the seed for Mersenne twister?


using the password, first character generated is 86;
let's see if we can replicate this in mersenne with seed using pycryptodome

maybe i can write a script to hook it instead?
i.e. hook every time generate_xor_fn is called with an x32dbg script

16 * 4= 64, so need 64 characters + hook to get all the mersenne characters 
0x401c61 is where to set up a breakpoint


Wane_1s_Adm1f1strnt0r
RealSecurePasswordlol
AAAAAAAABBBBBBBBAAAAAAAABBBBBBBBAAAAAAAABBBBBBBBAAAAAAAABBBBBBBB
