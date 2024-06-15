How to test exploit code that I have written exactly?
Ok, so I am using musl-gcc in order to do the compilation and whatnot 
Need to compile the exploit with the following flags:
musl-gcc exploit.c -static -pie -s -O0 -fPIE -o exploit 
How might I go about getting a shell? I need to get it in user space I think?
But I am in kernel space 
But nothing is enabled, so any code execution should allow me to do stuff in user space?

struct knote {
    char *data;
    size_t len;
    void (*encrypt_func)(char *, size_t);
    void (*decrypt_func)(char *, size_t);
};

8 bytes, 8 bytes, 8 bytes, 8 bytes = 32 bytes

struct knote_user {
    unsigned long idx;
    char * data;
    size_t len;
};
8 bytes, 8, 8 = 24 bytes

When we allocate a 32 byte or 24 byte block in the kernel, what happens?
What happens when the size of the data and the input length are not the same?
Goal is to overwrite a function pointer 
What is privesc_ctx_swp?
What happens when we do an allocation?

in order to set up debugging, need vmlinux-to-elf tool 
https://mudongliang.github.io/2022/06/07/RealWorldCTF-digging_into_kernel.html
Another useful writeup for kernel exploitation 
From the writeup, it seems that in order to permit debugging, we have to start as root user 
otherwise it won't work 
need to modify the init file 

ok we have prepare_kernel_creds and commit_creds.
These creds refer to user ids/group ids.
We prepare the creds structure used to change the credentials of the current process?
Return a pointer to a new cred structure.
One of the techniques uses a struct with function pointers, and the other technique uses the encrypt function which already exists in the kernel module.
Why is he doing a grep for asdf?
Is the code modifying a chunk of memory in the kernel?
I guess it would be "permanent" 

copy_from_user
    to: knotes[ku.idx]->data
    from: ku.data
    amnt: len 
when does this call fail? when copying from an invalid pointer?
When copying a length that is too large?
Need to see what happens when kfree is called 

Ok call kfree() twice and then what?
The memory is not zero-d out or anything by the allocator
For some reason, we need to set the breakpoint after getting into the exploit function 
Very hard to debug here 
kmalloc and kfree and not in the symbol table?
are they shorthands for other functions with underscores?
0xffffffff810c88f0  <-- looks like the addr for kfree

0xffffffffa00002ba    mov    rax, qword ptr [rax*8 - 0x5fffdc40]
   0xffffffffa00002c2    mov    rdi, qword ptr [rax]
   0xffffffffa00002c5    call   0xffffffff810c88f0            <0xffffffff810c88f0>
 
   0xffffffffa00002ca    mov    rax, qword ptr [rbp - 0x28]
   0xffffffffa00002ce    mov    rdi, qword ptr [rax*8 - 0x5fffdc40]
 ► 0xffffffffa00002d6    call   0xffffffff810c88f0            <0xffffffff810c88f0>
 
   0xffffffffa00002db    mov    rdi, 0xffffffffa0002100
   0xffffffffa00002e2    call   0xffffffff811fd220            <0xffffffff811fd220>
 
   0xffffffffa00002e7    mov    rax, 0xfffffffffffffff2 <-- this is the signal error value
   0xffffffffa00002ee    jmp    0xffffffffa00000c8            <0xffffffffa00000c8>

We can use the "search" command to find memory in pwndbg

knote_t payload;
    payload.data = "ABCDEFGH";
    payload.len = 8;
    knote_user_t to_send;
    to_send.idx = 0;
    to_send.data = (char*)&payload;
    to_send.len = 8; // not sure why there are two length values but whatever
    // it's because I misunderstood the problem; knote_user is all we need from user space

the knote struct is only used in kernel space
those values are pretty consistent 
it might be because the memory was freed 
so there is probably some pointer that points to the thing that points to 0x5ed...90
pwndbg> search --hex ffff8880075bed98
Searching for value: b'\xff\xff\x88\x80\x07[\xed\x98'


Actually use this instead:
pwndbg> search --qword 0xffff8880075bed98
Searching for value: b'\x98\xed[\x07\x80\x88\xff\xff'
[pt_ffff888000000] 0xffff888000093c00 0xffff8880075bed98

Need to figure out if the placements of the buffers is 
0        1
--- OR  ---
1        0
(the numbers are the indices)

0xffff888000093be0:  0xffffea00001d8b40 0xffffea00001d8b80
0xffff888000093bf0:  0xffffea00001d8bc0 0xffffea00001d8600
0xffff888000093c00:  0xffff8880075bed98 0x0000000000000008
0xffff888000093c10:  0xffffffffa0000000 0xffffffffa0000020
0xffff888000093c20:  0xffff8880075beda0 0x0000000000000008
0xffff888000093c30:  0xffffffffa0000000 0xffffffffa0000020 <-- i think these are function pointers

0 / 1 ordering 
Interestingly, the strings also come one after the other


0xffff888000093c00  -> 0xffff8880075bed98 BBBBDDDD

memory before free is called
0xffff888000093bc0:  0xffffea00001d8700 0xffffea00001d84c0
0xffff888000093bd0:  0xffffea00001d85c0 0xffffea00001d8b00
0xffff888000093be0:  0xffffea00001d8b40 0xffffea00001d8b80
0xffff888000093bf0:  0xffffea00001d8bc0 0xffffea00001d8600
0xffff888000093c00:  0xffff8880075bed98 0x0000000000000008
0xffff888000093c10:  0xffffffffa0000000 0xffffffffa0000020

memory after free is called
0xffff888000093bc0:  0xffffea00001d8700 0xffffea00001d84c0
0xffff888000093bd0:  0xffffea00001d85c0 0xffffea00001d8b00
0xffff888000093be0:  0xffffea00001d8b40 0xffffea00001d8b80
0xffff888000093bf0:  0xffffea00001d8bc0 0xffffea00001d8600
0xffff888000093c00:  0xffff8880075bed98 0x0000000000000008

doesnt seem liek anything changed after the second free
Why is the value stored in the knotes structure twice?
What is the seq_operations structure?


Before the delete call()
pwndbg> x/20gx 0xffff888000093bd0
0xffff888000093bd0:  0xffffea00001d85c0 0xffffea00001d8440
0xffff888000093be0:  0xffffea00001d8b00 0xffffea00001d8b40
0xffff888000093bf0:  0xffffea00001d8b80 0xffffea00001d8bc0
0xffff888000093c00:  0xffff8880075bed98 0x0000000000000008
0xffff888000093c10:  0xffff888000093c20 0x0000000000000000
0xffff888000093c20:  0x0000000000000000 0x0000000000000000
0xffff888000093c30:  0xffff888000093c40 0x0000000000000000

After the delete call
0xc00 appears twice?
going to assume it is the "next pointer" in the free list
0xffff888000093bd0:  0xffffea00001d85c0 0xffffea00001d8440
0xffff888000093be0:  0xffffea00001d8b00 0xffffea00001d8b40
0xffff888000093bf0:  0xffffea00001d8b80 0xffffea00001d8bc0
0xffff888000093c00:  0xffff8880075bed98 0x0000000000000008
0xffff888000093c10:  0xffff888000093c00 0x0000000000000000
0xffff888000093c20:  0x0000000000000000 0x0000000000000000
0xffff888000093c30:  0xffff888000093c40 0x0000000000000000
0xffff888000093c40:  0x0000000000000000 0x0000000000000000
0xffff888000093c50:  0xffff888000093c60 0x0000000000000000
0xffff888000093c60:  0x0000000000000000 0x0000000000000000

Also observe that 98 -> 98 instead of to a0 which is what the expected behavior is 
0xffff8880075bed98:  0xffff8880075bed98 0xffff8880075beda8
0xffff8880075beda8:  0xffff8880075bedb0 0xffff8880075bedb8

/* knote_user_t to_send; */
    /* def.idx = 0; */
    /* def.data = "AAAAAAAA"; */
    /* def.len = 8; */
    // where is knote_encrypt actually located though?
    // is it supposed to be somewhere 
    // ffffffffa0000020 t knote_decrypt        [knote]
    // ffffffffa0000000 t knote_encrypt        [knote]

general protection fault, probably for non-canonical address 0x4444444442424252: 0000 [#1] NOPTI
Not sure what the 52 is 

faults at FFFFBBBB?

use modprobe_path for something 
what is modprobe_path?
rop gadget 
ok so this technique in particular uses the prepare_kernel_cred technique and commit_creds technique 
I think both are outdated but w/e 

setxattr is a system call used to set an extended attribute of a file?
not sure what an extended attribute is exactly
they are used to store metadata not typically included in standard file attributes
These attributes can be used by various applications for diff purposes
https://lkmidas.github.io/posts/20210223-linux-kernel-pwn-modprobe/
    <-- very good writeup
What is needed to return into userland?
modprobe_path is needed 
i dont really understand how the rdi gadget is used 
i understand that we have to call a function that modifies modprobe_path since modprobe_path is invoked whenever a file with an unknown file header is executed but what is in rdi/rsi when the encrypt() function is called?
protection fault is trippered at some address, and the rdi and rsi are two random values 
i guess when encrypt() is called, it uses data as arg1, and len as arg2 
so it kind of makes sense that i would be able to overwrite modprob_path with the value at rsi







# TODO:
- [x] get a file executing in the kernel 
- [x] break on kmalloc 
- [x] Set up debugging for qemu via gdb 
    <-- turns out I was compiling the file stripped instead of unstripped 
- [x] Figure out what the bug is 
    <- KNOTE_CREATE with an error, followed by KNOTE_DELETE for a double free
- [x] Find a way to step around the user code 
- [ ] trigger the bug? 
    What is the bug? The bug is from knote_create; fail copy_from_user and do a free 
- [ ] Find the knotes array in memory, and print out the value at idx 0
- [ ] Examine what kfree-d data looks like 


Commands:
To compile exploit: 
    musl-gcc exploit.c -static -pie -s -O0 -fPIE -o exploit
    <-- the -s flag strips the binary and removes the symbols so we should probably get rid of that instead

To convert the filesystem to something useable: 
    find . -print0 | cpio --null --format=newc -o | gzip -9 > ../new-rootfs.cpio.gz

https://ptr-yudai.hatenablog.com/entry/2020/03/16/165628
https://sam4k.com/like-techniques-modprobe_path/ <-- modprob path kernel exploit?

Important to note that we dont need to call delete() because this is what happens
order:
0th index:
kmalloc(0x20 data)
kmalloc(0x20 struct) (struct contains data)

kfree(0x20 data) 
kfree(0x20 struct)

kmalloc(0x20 data) <-- uses the kfree struct 
kmalloc(0x20 struct) <-- uses the kfree data location 





