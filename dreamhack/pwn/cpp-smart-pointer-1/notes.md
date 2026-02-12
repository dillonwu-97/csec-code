maybe the attack vector is something like 

create two ptrs to same object 
reset() which frees the object
malloc to write into the memory?
then call the fn somehow once we write data into the mem?
maybe something like this
 

what tools do i have?
- reset pointer which frees 
- reassign a pointer
- call a pointer 
- need multiple things to point to the same thing 


1) change 1 -> banana
2) test smart pointer hits 617 

delete 1 -> test 1 -> gives dereference 0
delete 1 -> test 2 -> fail at 0x617
delete 1 -> malloc -> malloc again -> test 2  -> 0x42424242




