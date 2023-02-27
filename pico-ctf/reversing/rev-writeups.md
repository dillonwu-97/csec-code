---
title: reversing
description: Reversing challenges from pico-ctf
tags: reversing, shell
---

### ARMsembly0
The flag is picoCTF{6D1D2DD1}. The notes of this can be found in the arm0 shellcode in csec-code.

### vault-door-training
Just look at the code. The flag is picoCTF{w4rm1ng\_Up\_w1tH\_jAv4\_be8d9806f18}.

### vault-door-1
A quick gander at the code reveals the flag is picoCTF{d35cr4mbl3\_tH3\_cH4r4cT3r5\_75092e}.

### asm1
We pass in the argument 0x2e0.
The code is as follows:  
asm1:  
	<+0>:	push   ebp <--push base pointer  
	<+1>:	mov    ebp,esp <-- move address of stack pointer into base pointer location, i.e. set the base pointer equal to the stack pointer  
	<+3>:	cmp    DWORD PTR [ebp+0x8],0x3fb <-- the stack grows DOWN, so ebp + 0x8 is the first argument of the function, i.e. 0x2e0.  
	<+10>:	jg     0x512 <asm1+37> <-- jump if 0x2e0 > 0x3fb  
	<+12>:	cmp    DWORD PTR [ebp+0x8],0x280   
	<+19>:	jne    0x50a <asm1+29> <-- jump if 0x2e0 != 0x280  
	<+21>:	mov    eax,DWORD PTR [ebp+0x8]  
	<+24>:	add    eax,0xa  
	<+27>:	jmp    0x529 <asm1+60>  
	<+29>:	mov    eax,DWORD PTR [ebp+0x8] <-- arrived from asm1+19  
	<+32>:	sub    eax,0xa <-- 0x2e0 - 0xa = 0x2d6  
	<+35>:	jmp    0x529 <asm1+60> <-- go to asm1+60  
	<+37>:	cmp    DWORD PTR [ebp+0x8],0x559  
	<+44>:	jne    0x523 <asm1+54>  
	<+46>:	mov    eax,DWORD PTR [ebp+0x8]  
	<+49>:	sub    eax,0xa  
	<+52>:	jmp    0x529 <asm1+60>  
	<+54>:	mov    eax,DWORD PTR [ebp+0x8]  
	<+57>:	add    eax,0xa  
	<+60>:	pop    ebp  
	<+61>:	ret      
  
The flag is 0x2d6.

### vault-door-2
I wrote a short snippet of code to reverse the steps outlined in the Java code. 

```python
rev = "jU5t\_a\_sna\_3lpm18g947\_u\_4\_m9r54f"
orig = [i for i in "jU5t\_a\_sna\_3lpm18g947\_u\_4\_m9r54f"]
for i in range(31, 16, -2):
    orig[i] = rev[i]
for i in range(16, 32, 2):
    orig[46-i] = rev[i]
for i in range(8, 16):
    orig[23-i] = rev[i]
for i in range(0,8):
    orig[i] = rev[i]
print("".join(orig))
```
The flag is picoCTF{jU5t\_a\_s1mpl3\_an4gr4m\_4\_u\_79958f}

### asm2
The argument 0x4, 0x2d is passed.
asm2:  
	<+0>:	push   ebp  
	<+1>:	mov    ebp,esp <-- set the address of the base pointer equal to that of the stack pointer  
	<+3>:	sub    esp,0x10 <-- subtract 0x10 from the stack pointer  
	<+6>:	mov    eax,DWORD PTR [ebp+0xc] <-- set the value of eax equal to the second argument  
	<+9>:	mov    DWORD PTR [ebp-0x4],eax <-- move the value at eax into the first four bytes of the stack  
	<+12>:	mov    eax,DWORD PTR [ebp+0x8] <-- move the value of the first argument to eax  
	<+15>:	mov    DWORD PTR [ebp-0x8],eax <-- move the  value at eax to the second four bytes of the stack    
	<+18>:	jmp    0x50c <asm2+31> <-- go to asm2+31  
	<+20>:	add    DWORD PTR [ebp-0x4],0x1 <-- add 0x1 to stack[0] / 0x2d  
	<+24>:	add    DWORD PTR [ebp-0x8],0xd1 <-- add 0xd1 to stack[1]  / 0x4
	<+31>:	cmp    DWORD PTR [ebp-0x8],0x5fa1   
	<+38>:	jle    0x501 <asm2+20> <-- check if 0x4 <= 0x5fa1  
	<+40>:	mov    eax,DWORD PTR [ebp-0x4] <-- move value at stack[0] into eax / return value; it is a counter of the number of iterations in the loop  
	<+43>:	leave  
 	<+44>:	ret    

Do (0x5fa1 - 0x4) / (0xd1) = 117.1 rounded up to 118.
118 + 45 = 163 = 0xa3

Reminder: the order is (lower memory) -> local memory -> base pointer -> return address -> arg1 -> arg2 -> (higher memory)

The flag is 0xa3.

### vault-door-4
Convert the bytes to ascii to get the flag which is picoCTF{jU5t\_4\_bUnCh\_0f\_bYt3s\_8f4a6cbf3b}.

### asm3

The program takes the arguments 0xd73346ed 0xd48672ae 0xd3c8b139.
asm3:
	<+0>:	push   ebp
	<+1>:	mov    ebp,esp
	<+3>:	xor    eax,eax <-- eax is now zero
	<+5>:	mov    ah,BYTE PTR [ebp+0xa]  <-- assuming little endian, move 0x33 to register ah
	<+8>:	shl    ax,0x10 <-- shift left <-- number at ax shifted to the left by 16 bits and zeroed out
	<+12>:	sub    al,BYTE PTR [ebp+0xc] <-- subtract 0xae from register al
	<+15>:	add    ah,BYTE PTR [ebp+0xd] <-- add 0x72 to register ah
	<+18>:	xor    ax,WORD PTR [ebp+0x10] <-- xor 0xb139 with register ax
	<+22>:	nop
	<+23>:	pop    ebp
	<+24>:	ret    

This website is good at explaining the parts of the eax register: <a href="https://www.cs.uaf.edu/2017/fall/cs301/lecture/09_11_registers.html#:~:text=It%20was%20added%20in%202003,transition%20to%2064%2Dbit%20processors.&text=ax%20is%20the%2016%2Dbit,is%20the%20high%208%20bits."> https://www.cs.uaf.edu/2017/fall/cs301/lecture/09_11_registers.html#:~:text=It%20was%20added%20in%202003,transition%20to%2064%2Dbit%20processors.&text=ax%20is%20the%2016%2Dbit,is%20the%20high%208%20bits. </a>

Important note: The first argument starts at ebp + 8 and ends at ebp + 12
The stack looks like this:
low memory --> high memory
   0->4     4->8    8  9  a  b    c  d  e  f   10 11 12 13  
ebp(4) | ret (4) | ed 46 33 d7 | ae 72 86 d4 | 39 b1 c8 d3 

<+5> 0x33 = 0b 0011 0011
<+8> 0011 0011 0000 0000 0000 0000 (Question: Does 0011 0011 get shifted, or does it actually disappear?)
<+12> 0x00 - 0xae = -0xae = -174 => (two's complement) => 0x152 => get rid of the overflow bit!
<+15> 0x00 + 0x72 = 0x72
<+18> 0xb139 ^ 0x7252 = 0xc36b

Note: It seems that the shift left operation gets rid of 0x33, but I'm not entirely sure why.

Extra:
Additionally, we can also create a program that runs the shell code. The code can be found here: 
<a href="https://github.com/dillonwu-97/csec-code/tree/main/pico-ctf/reversing/asm3"> https://github.com/dillonwu-97/csec-code/tree/main/pico-ctf/reversing/asm3 </a>

The commands on the terminal for compilation are:  
gcc -masm=intel -m32 -c test.S -o test.o  
gcc -m32 -c main.c -o main.o  
gcc -m32 test.o main.o -o main  
-m32 is used to compile 32 bits objects on a compiler configured to compile 64 bits objects by default.

### vault-door-5
First, base64 decode the string. The string %% is just string formatting for the % symbol. Split along %, and then convert the hex to ascii to get the flag, which is picoCTF{c0nv3rt1ng_fr0m_ba5e_64_e3152bf4}.

### vault-door-6
For this puzzle, just xor each of the hex values to get the original password. The flag is picoCTF{n0t_mUcH_h4rD3r_tH4n_x0r_948b888}.

### vault-door-7
```java
public int[] passwordToIntArray(String hex) {
    int[] x = new int[8];
    byte[] hexBytes = hex.getBytes();
    for (int i=0; i<8; i++) {
        x[i] = hexBytes[i*4]   << 24
                | hexBytes[i*4+1] << 16
                | hexBytes[i*4+2] << 8
                | hexBytes[i*4+3];
    }
    return x;
}

public boolean checkPassword(String password) {
    if (password.length() != 32) {
        return false;
    }
    int[] x = passwordToIntArray(password);
    return x[0] == 1096770097
        && x[1] == 1952395366
        && x[2] == 1600270708
        && x[3] == 1601398833
        && x[4] == 1716808014
        && x[5] == 1734304867
        && x[6] == 942695730
        && x[7] == 942748212;
}
```
```python
x = [0]* 8
x[0] = 1096770097
x[1] = 1952395366
x[2] = 1600270708
x[3] = 1601398833
x[4] = 1716808014
x[5] = 1734304867
x[6] = 942695730
x[7] = 942748212
ret = [''] * 32
for i in range(8):
    for j in range(4):
        ret[4*i + j] = hex(x[i])[2:][2*j:2*j+2]
print("".join(ret))
print(bytes.fromhex("".join(ret)).decode("ascii"))
```
I examined the code, and found the flag. The flag is picoCTF{A_b1t_0f_b1t_sh1fTiNg_dc80e28124}.

### asm4
asm4("picoCTF_a3112") is the function being run.


Memory looks like:
low memory -> high memory
  -0x10  -0xc  -0x8 -0x4   0    +0x4   8   c  10  14  18  1c   20  24  28  2c 30  34  38
| 0x246 | 0x0 |    |    | ebp | ret  | 2 | 1 | 1 | 3 | a | _ | F | T | C | o | c | i | p
