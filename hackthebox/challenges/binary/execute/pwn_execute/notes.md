char blacklist[] = "\x3b\x54\x62\x69\x6e\x73\x68\xf6\xd2\xc0\x5f\xc9\x66\x6c\x61\x67";

3b = 59
3b 54 62 = cmp 
/bin/sh = 62 69 63 73 68 
f6
d2 = rdx
c0 = rax
5f = pop 
c9 = leave
66 = 
6c 
61 = popad
67 = 


idea is to write code onto the stack and xor with another value 


shellcode: 


execve: 
rax = 59, 
'/bin/sh'
