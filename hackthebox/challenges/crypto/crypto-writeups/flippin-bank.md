---
title: flippin-bank
description: twoforone
tags: cbc, crypto, byte at a time
---
The attack involved in this exploit is the byte-at-a-time attack. The byte-at-a-time attack involves corrupting a single bit in the ciphertext with the goal of changing the plaintext when it is decrypted. In this particular exercise, the code checks for the string "admin&password=g0ld3n\_b0y" when decrypting the ciphertext, and if it sees the string, the user is authenticated. However, inputting just "admin&password=g0ld3n\_b0y" results in an error. Instead, the attacker must input something like "bdmin&password=g0ld3n\_b0y" and then corrupt the first letter of the input so that is is "a" instead of "b."

A good resource for understanding the attack can be found here: <a href="https://resources.infosecinstitute.com/topic/cbc-byte-flipping-attack-101-approach/"> https://resources.infosecinstitute.com/topic/cbc-byte-flipping-attack-101-approach/ </a>.  

There are several observations to be made: 
1) when the query "logged\_username=bdmin&password=g0ld3n\_b0y" is encrypted, it is done so in CBC mode. 
2) each block will be 16 bytes, with the final block being padded until it is 16 bytes using pkcs7 padding.
3) logged\_username is 16 bytes long, so "bdmin..." will start immediately on the next block.

The CBC encryption mode is also described in the diagram below:   

<img src = "/csec-writeups/hackthebox/htb-crypto/flippinbank-2.png" />

The decryption process is outlined below: 

<img src = "/csec-writeups/hackthebox/htb-crypto/flippinbank-3.png" />

As we can see, in the decryption process, 
1) the first 16 bytes of ciphertext will be used to xor the key and second 16 bytes of ciphertext in the decryption process, i.e. C0 ^ C1 ^ key = P1, where C is ciphertext and P is plaintext.
2) each xor byte lines up, i.e. byte 1 in block 1 is used to xor byte 1 in block 2. 
This means that in order to change the encrypted "b" value in the second block, we just have to xor the encrypted "l" value in the first block. 
3) ord("b") is 98. ord("a") is 97. 97 ^ 98 = 3. Therefore, we just have to xor C0 with the value 3, and P1 will be changed as well.

I saw that the leaked ciphertext was aa49b0add22457ceb21b45528779851507619d2d2e0d6f9da2f5ee950a147530a67b457d31e379a86ae743de0db8a1e3. 

int("aa", 16) = 170, 170 ^ 3 = 169, and 0xaa - 0x01 = 0xa9.

I changed the first byte so that it became a949b0add22457ceb21b45528779851507619d2d2e0d6f9da2f5ee950a147530a67b457d31e379a86ae743de0db8a1e3. 

<img src = "/csec-writeups/hackthebox/htb-crypto/flippinbank-1.png" />

The flag is HTB{b1t\_fl1pp1ng\_1s\_c00l}. 

Note: The key and IV value used each time the remote server is started will be different so copy and pasting won't work. 

Finally, the code in this link is the sandbox I used to look at how the ciphertext responded to different instances of byte corruption. 
<a href="https://github.com/dillonwu-97/csec-code/blob/main/hackthebox/challenges/crypto/flippinbank.py"> https://github.com/dillonwu-97/csec-code/blob/main/hackthebox/challenges/crypto/flippinbank.py </a>