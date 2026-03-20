there are byte differences in some of the files


b/t 150 and 153

addr           154            150
6e8f8          68             ff       
1309c1         94             5c
1b19a9         96             84
286162         43             0d

addr          153             150 
1309c1        94              5c 
1b19a9         96             84
286162        43              0d 

incrementally adding changes it looks like 
order:
1309c1, 286162, 1b19a9, 6e8f8


# Questions
- How is it choosing what to write, and why is it writing that value

0019FC04 00A55D28 L"\\\\?\\C:\\Users\\spect\\Desktop\\4_-_UnholyDragon\\UnholyDragon-1.exe"

why is \\\\?\\ added to the beginning of the string
https://stackoverflow.com/questions/21194530/what-does-mean-when-prepended-to-a-file-path
doing something with a very long path i guess?
creating multiple files, but do what end?

006D7720  45 21 40 00 AB AB AB AB AB AB AB AB 00 00 00 00  E!@.««««««««....  
006D7730  00 00 00 00 00 00 00 00 87 B3 B6 96 E5 CC 00 18  .........³¶.åÌ..  
006D7740  20 56 69 00 02 00 00 00 8C 65 69 00 01 00 00 00   Vi......ei.....  
006D7750  10 56 69 00 01 00 00 00 70 55 69 00 01 00 00 00  .Vi.....pUi.....  
006D7760  70 55 69 00 01 00 00 00 08 56 69 00 04 00 00 00  pUi......Vi.....  
006D7770  00 56 69 00 06 00 00 00 F8 55 69 00 06 00 00 00  .Vi.....øUi.....  
006D7780  F0 55 69 00 07 00 00 00 E0 55 69 00 07 00 00 00  ðUi.....àUi.....  
006D7790  E8 55 69 00 06 00 00 00 AB AB AB AB AB AB AB AB  èUi.....««««««««  
006D77A0  00 00 00 00 00 00 00 00 87 B3 B6 96 EF D9 00 18  .........³¶.ïÙ..  

these look like bytes of some kind? not sure 


looks there are certain opcodes being flipped or something?G
not sure what is being flipped, and if i need to disassemble all of them or something like that 
there are also exceptions that occur, but not sure why so that is worth checking out as well i think 


looks like there is some packed stuff at 40ce5c or something? not sure 
okay, so 150 was generated from executing the original i guess? but renaming it also changed the functionality? so it's just flipping bytes in memory or something like that
what part of the code is responsible for writing stuff?

TODO: check if original 150 and new 150 are the same files, also 
yea i def need to patch the file somehow 

dr4g0n_d3n1al_of_s3rv1ce@flare-on.com

okay, i jsut changed the name and header and it worked 
