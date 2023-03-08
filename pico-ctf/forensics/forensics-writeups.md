---
title: forensics
tags: forensics
---

### Glory of the Garden
strings garden.jpg | grep pico. The flag is picoCTF{more_than_m33ts_the_3y3eBdBd2cc}.

### So Meta  
exiftool pico_img.jpg. The artist of the photo is picoCTF{s0_m3ta_eb36bf44}. 

### shark on wire 1  
Follow a random UDP stream, and cycle through them. I found that udp.stream eq 6 contains the flag: picoCTF{StaT31355_636f6e6e}.  

### extensions
I ran xxd flag.txt, and saw the first few letters of the plaintext hexdump was .PNG. I saved the flag.txt file as 
a .png file instead, and opened it. The flag is picoCTF{now_you_know_about_extensions}.

### What Lies Within
I tried using the commands exiftool, file, mdls, xattr but none of the command line tools reveal anything. 
Instead, this flag relies on the use of steganography. The picture is modified using the Least Significant Bit algorithm. 
A quick online decoder like the one at <a href="https://stylesuxx.github.io/steganography/">https://stylesuxx.github.io/steganography/ </a> will reveal the hidden message. The flag is picoCTF{h1d1ng_1n_th3_b1t5}. 
Additionally, the link here provides a good description of the encoding method: <a href="https://www.boiteaklou.fr/Steganography-Least-Significant-Bit.html#do-it-yourself">
https://www.boiteaklou.fr/Steganography-Least-Significant-Bit.html#do-it-yourself </a>. The command line tool zsteg is also useful; you can just do 
zsteg buildings.png. 

### c0rrupt

I used the following links to learn about png file formats. 
<a href="https://stackoverflow.com/questions/58150200/how-to-change-file-header-in-terminal"> https://stackoverflow.com/questions/58150200/how-to-change-file-header-in-terminal </a>
<a href="http://www.libpng.org/pub/png/spec/1.2/PNG-Structure.html"> http://www.libpng.org/pub/png/spec/1.2/PNG-Structure.html </a>
<a href="http://www.libpng.org/pub/png/spec/1.2/PNG-Chunks.html"> http://www.libpng.org/pub/png/spec/1.2/PNG-Chunks.html </a>
<a href="https://www.w3.org/TR/2003/REC-PNG-20031110/"> https://www.w3.org/TR/2003/REC-PNG-20031110/ </a> Section 5.6 shows the different possible names of chunks


First, I created a hexdump using the command xxd mystery > tmp.
I saw from IEND that the file was most likely a png file. The first thing I did was to change the extension 
at the start of the hexdump so that it reflected .png instead of .eN4. This involves replacing the first eight bytes with 
89  50  4e  47  0d  0a  1a  0a. 

Next, I converted the hexdump back into a png file using xxd -r tmp > solve.png. I then used the command pngcheck -vvv solve.png 
to see what other errors existed in the png file. The next error is that there is an invalid chunk name: C"DR. Instead of C"DR, the chunk name should be 
IHDR. 

<img src = "/csec-writeups/pico-ctf/forensics/corrupt-1.png"> <br/>

This is because after identifying that the file is a .png file, the chunks begin with IHDR, and end with IEND. Since there is not IHDR chunk, the C"DR error must be pointing 
to the fact that it is a corrupted IHDR chunk. I changed the two bytes to 4948. 

I ran the code again. This time, I saw that there was a CRC error in chunk pHYs. It states that the computed value is 
38d82c82, and that the expected value is 495224f0. 

<img src = "/csec-writeups/pico-ctf/forensics/corrupt-2.png"> <br/>

After examining the hexcode again, I saw the sequence of bytes 495225f0, and replaced these bytes 
with 38d82c82. The reason I made this replacement is that the original values were a checksum that was calculated incorrectly. The checksum is calculated 
using the CRC algorithm.  

The final error I received was one that stated "invalid chunk length (too large)". 

<img src = "/csec-writeups/pico-ctf/forensics/corrupt-3.png"> <br/>

Starting from the pHYs chunk, I saw from the output of pngcheck that 
the the total size of the chunk is 4 bytes (length) + 4 bytes (chunk type) + 9 bytes (chunk data, size specified from pngcheck) + 4 bytes(crc check) = 21 bytes. 
The next chunk starts at aa aa ff a5 (size of chunk), followed by ab 44 45 54 (type of chunk) and the ascii values of that is ".DET". Unfortunately, this is not the name of a chunk, so there must be an error here. 
The size of the chunk is also probably too large. 

From Table 5.3 in section 5.6, I saw that the ordering is .PNG -> IHDR -> pHYs -> IDAT -> IEND

It turns out that ".DET" should actually be "IDAT". The correct chunk size turns out to be 00 00 ff a5 and there are also a couple of ways to find this. You can repeatedly try different inputs until 
pngcheck returns no error, but the analytic solution would be to find the second "IDAT" location. This can be done using the command line tool 
binwalk, specifically  
binwalk -R "IDAT" solve.png  
to find the locations of "IDAT" in the photo. 

<img src = "/csec-writeups/pico-ctf/forensics/corrupt-4.png"> <br/>

After finding the locations, we can calculate the size of the first "IDAT" chunk 
by subtracting from the location of the second "IDAT" chunk, i.e. 0x10008 (start of second IDAT) - 0x04 (4 bytes specifying size of second IDAT) - 0x57 (start of first IDAT) - 0x04 (4 bytes for the name "IDAT") - 0x04 (4 bytes for tail end of the first "IDAT" / checksum)= ff a5.

The flag is picoCTF{c0rrupt10n\_1847995}.


### Whitepages 
I opened the whitepages.txt file and highlighted it, and saw that there were some dots. At first, I thought it was braille or morse code, but that was a dead end. It turns out 
that the file was just a sequence of 1's and 0's. I wrote a simple python script to find the ascii values for the binary sequence.  

<img src = "/csec-writeups/pico-ctf/forensics/whitepages.png"> <br/>

The flag is picoCTF{not\_all\_spaces\_are\_created\_equal\_3e2423081df9adab2a9d96afda4cfad6}

### like1000
I wrote a simple shell script to unzip the tar files. The flag is picoCTF{l0t5\_0f\_TAR5}

### 