00000010: 0301 0104 0101 0501 0106 0101 0701 0108  ................
00000020: 0201 0020 0106 0201 0102 0102 0201 0302  ... ............
00000030: 0104 0201 0502 0106 0201 0702 0108 0301  ................
00000040: 0003 0101 0301 0203 0103 0301 0403 0105  ................
00000050: 0301 0603 0107 0301 0804 0100 0401 0104  ................
00000060: 0102 0401 0304 0104 0401 0504 0106 0401  ................
00000070: 0704 0108 0501 0005 0101 0501 0205 0103  ................
00000080: 0501 0405 0105 0501 0605 0107 0501 0806  ................
00000090: 0100 0601 0106 0102 0601 0306 0104 0601  ................
000000a0: 0506 0106 0601 0706 0108 0701 0007 0101  ................
000000b0: 0701 0207 0103 0701 0407 0105 0701 0607  ................
000000c0: 0107 0701 0808 0100 0801 0120 0107 0801  ........... ....
000000d0: 0208 0103 0801 0408 0105 0801 0608 0107  ................
000000e0: 0801 0809 0100 0901 0109 0102 0901 0309  ................

observation of pattern: 
01 -> 02 -> 03 after each 00 so it increments
so maybe 00 is a delimiter for something 
the delimiter pattern for different values is different which is kinda weird

wtf is nested_call fn doing?

what are these weird math calculations
return but no idea what happened

doest seem like adding more characters grows the size of the file
compressing same file yields different output as well (sometimes)


0x55555555654c
b0 b0 e2 b0 b0 af af e0 af af ae ae de ae ae ad ad dc ad ad ac ac
pattern: pairs, and single decrement, also there is a double decrement for single chars

sub_555555556BC0 <- not sure what the numbers are honestly

not sure what this is doing honestly 
not sure how what this is doing is related to user input 
how is this even considered compression honestly 

okay, ai says we do some sort of huffman encoding maybe?

okay, so there is some buffer

okay, is this just reversing huffman coding? 
i think it is huffman encoding of various levels, i.e. n-ary encoding and we get a random value for the tree level so the solution might be understanding huffman coding at various levels and reversing that
okay, interesting
so there is a huffman tree in the comp and then also the table

idk why the path to the char "A" is 120 though since 0x2d = 45 => (ternary) => 120 

Okay the writes seem to be COMP + nodes_per_level + node_count in bytes of 2, followed by 1?

maybe not exactly huffman coding because there is a value at each node?
okay,how is the tree connected now?

020100
020101
020102
020103
020104
400102 <-- why is there a break in the pattern here?
030100
030101
030102
030103
030104
400103

okay, i think i have the solution, but not sure what the best implementation is

max value is the root node 

need to know what the exact padding is

is there something in the code that is making this something else?? e.g. making it so that if the compression is not 3, adds an extra step or something
cuz the alg def works for n = 3

trying to figure out how the conversion works; if rev the calculation, can recover the original int i think 


# 3/13
- so the root node is not included 
- so we grab the parent which is the leftmost two bytes 
- the rightmost is the order 
- trying to figure out if the root node is 0 or max number
- so what we have is each leaf i think?
- so the 0th value is leaf_0, leaf_1 ... 
- how to link all of the nodes together?
- I think it should be in base 5 as opposed to base 

# 3/17
- Maybe it's just max bit representation for 256 or something
- maybe the packing ratio is used to determine the number of bytes written
- yea i think this is the case
- 0xf -> 0x100000002 -> 0x1
- 0xd -> 0x100000002 -> 0x1
- 0xb -> 0x400000009 -> 0x4
- 0x9 -> 0x200000005 -> 0x2
- 0x7 -> 0x40000000b -> 0x4
- 0x5 -> 0x30000000a -> 0x3
- 0x3 -> 0x100000005 -> 0x1

the upper byte is definitely the number of bytes written, but what is the lower byte used for?
the lower byte is the number of iterations of something, probs the number of iterations we can run to compress some values before hitting a limit  

read number of bytes -> convert to base n 

missing some values for some reason, but not sure why
where am i losing info v confused

error in alg is that root should be max parent, not necessarily last element in the list i think 

# Questions
- [ ] What is causing the output to be different on diff runs? 
    <- could it be the randomization value?
- [ ] What is causing the buffer to expand? 
    -> it is n-ary encoding
- [ ] what is the boundary byte?

# TODO
- [ ] need to separate the tree from the compressed data
    - [ ] Where is tree constructed?
    - [ ] where is actual data?
