Cut the blocks based on 

cmp edx, eax 
setnz al 
test al, al 
jnz loc_5555
    

.text:0000555555556D1D                 db 39h
.text:0000555555556D1E                 db 0C2h
.text:0000555555556D1F                 db 0Fh
.text:0000555555556D20                 db  95h
.text:0000555555556D21                 db 0C0h
.text:0000555555556D22                 db 84h
.text:0000555555556D23                 db 0C0h
.text:0000555555556D24                 db 0Fh
.text:0000555555556D25                 db  85h
.text:0000555555556D26                 db  4Fh ; O
.text:0000555555556D27                 db  87h
.text:0000555555556D28                 db    2
.text:0000555555556D29                 db    0

cut based on these bytes

there may be some chunks that dont obey this heuristic though


0x0:    test       dword ptr [rdx], edi <- there is this randomly


# 1/28
if we see the call instruction, then replace with string alloc?; no i think we just access a position in the str
take a position of something 
and there where is the check?
we use this value 370287DEECEA9AF1h

implementation:
1) set up memory for each block 
2) replace the call instruction to just grab the byte at position in esi 
3) set up spin loop for all ascii characters 






00005555555563BD <- breakpoint

https://stackoverflow.com/questions/57110383/x86-multiplication-with-3-imul-vs-shl-add


different disassembly found:
in ida: 
movzx   eax, byte ptr [rax]
.text:0000555555556448                 movsx   eax, al
.text:000055555555644B                 imul    eax, 42h ; 'B'
.text:000055555555644E                 add     ebx, eax
.text:0000555555556450                 lea     rax, [rbp+some_store]
.text:0000555555556454                 mov     esi, 5
.text:0000555555556459                 mov     rdi, rax


Addr: 0x555555556445 movzx eax, byte ptr [rax]
Nothing 
0x555555556448 3
Addr: 0x555555556448 movsx edx, al
Nothing 
0x55555555644b 2
Addr: 0x55555555644b mov eax, edx
Nothing 
0x55555555644d 2
Addr: 0x55555555644d add eax, eax
Nothing 
0x55555555644f 2
Addr: 0x55555555644f add eax, edx
Nothing 
0x555555556451 3
Addr: 0x555555556451 shl eax, 5
Nothing 
0x555555556454 2
Addr: 0x555555556454 add ebx, eax
Nothing 
0x555555556456 4
Addr: 0x555555556456 lea rax, [rbp - 0x50]
Nothing 
0x55555555645a 5
Addr: 0x55555555645a mov esi, 5
Nothing 
0x55555555645f 3
Addr: 0x55555555645f mov rdi, rax
Nothing 
0x555555556462 5
Addr: 0x555555556462 call 0x28259


in  unicorn
0x88:    movzx      eax, byte ptr [rax]
0x8b:    movsx      edx, al
0x8e:    mov        eax, edx
0x90:    add        eax, eax
0x92:    add        eax, edx
0x94:    shl        eax, 5
0x97:    add        ebx, eax
0x99:    lea        rax, [rbp - 0x50]
0x9d:    mov        esi, 5
0xa2:    mov        rdi, rax


does unicorn do optimizations?
no actually ida does

unicorn output:
0x9b975
0xece971b1

^-- diff from what i ahve 

*RAX  0x9c1a8
 RBX  0x8ca40
 RCX  0x78
 RDX  0x8fb9e
 RDI  0x7fffffffd980 —▸ 0x555555596750 ◂— 'ABCDEFGABCDEFGABCDEFGABCDEFGABCDEFGABCDEFGABCDEFGABCDEFGABCDEFGABCDEFG'
 RSI  0x45
 R8   0x7ffff7ca38c0 (_nl_C_LC_CTYPE_class+256) ◂— 0x2000200020002
 R9   7
 R10  0x555555596700 ◂— 0x555555596
 R11  0x46
 R12  1
 R13  0
 R14  0xc8312bcfabcb5fc8
 R15  0x370287deece3e277
 RBP  0x7fffffffd9d0 —▸ 0x7fffffffda70 —▸ 0x7fffffffdad0 ◂— 0
 RSP  0x7fffffffbbb0 ◂— 0
*RIP  0x555555556d1d ◂— cmp edx, eax

cmp inst 0x555555556d17 

maybe the initial state needs to be preserved which i wasnt expecting?

need to double check about that setup

000055555555625F <-- start 

i am uncertain about whether previous memory was modified or not

i think i might need to use the full code instead of just chunks 
set watchpoints to figure out if the memory that stores special values is used later on
stitch together other parts of the code

i am confused about where i have a mistake 

the idea that immediately comes to mind is building a sat solver but im not sure how i would get all of the obfuscation operations out
looks like they are all just multiplication?
cannot loop over them singly 
system of equations has 70 unknowns,  

edx holds our calculated value 
eax should contain correct result but not sure how calculated

i dont understand how the final value is constructed


1       breakpoint     keep y   0x00005555555563bd 
        breakpoint already hit 1 time
2       breakpoint     keep y   0x0000555555556d17 
3       breakpoint     keep y   0x0000555555556229 
        breakpoint already hit 1 time
12      breakpoint     keep y   0x0000555555556c16 
        breakpoint already hit 1 time
13      breakpoint     keep y   0x000055555555754e 

set $rip=0x0000555555556D2A


0x370287DEECEA23DF
0x370287deeceadb1a           <- second val
370287DEECE971B1h <- each rax value is different

xmm0 = looks like r14 is the first half, and the second half is rax 
xmm1 = r14 joined by r15
then xor the two 

looks like we do xor of two constant values, and match with sum of products


next steps:
1) create matrix and solve using products because i think we have a square matrix

I have assembly that performs shift + addition.
i need to lift these assembly snippets to multiplication
what python tool can i use to convert something like this:
mov eax edx
shl eax 3
add edx eax
to 
imul edx, 9


# TODO:
- [ ] get the imul, if imul doesnt exist, strong reduce 
- [ ] build the square matrix, find the inverse give flag

# 2/3
- split on the call op
- check for move esi, __ operation to see what gets modified
- observation: 0x16 and 0x20 are missing 

first is always imul ebx, eax, val because ebx stores the sum for later use

Tomorrow, grab the final values as well

rewrite code so that it splits using 

































