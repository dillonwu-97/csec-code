---
title: block-ciphers
description: cryptohack block cipher ctfs
tags: block ciphers, aes, crypto
---
### <ins> AES </ins>
1. crypto{bijection}
2. crypto{biclique}
3. crypto{inmatrix}
4. crypto{r0undk3y}
5. crypto{MYAES128}

### <ins> Block Cipher Modes </ins>
1. crypto{bl0ck_c1ph3r5_4r3_f457_!}
2. crypto{k3y5__r__n07__p455w0rdz?}

### <ins> ECB </ins>
1. The flag is crypto{p3n6u1n5_h473_3cb}. This is a byte-at-a-time attack.


### <ins> CTR </ins>
1. I saw that the counter was not being incremented so the png file was just encoded in ECB mode. I also noticed that it was a PNG file and know that the first 16 bytes of the header of a PNG file are constant. I decrypted the hexdump and outputted the original file, revealing the flag crytpo{hex_bytes_beans}. 
2. This is a great explanation of the attack: <a href="https://shainer.github.io/crypto/2017/01/02/crime-attack.html"> https://shainer.github.io/crypto/2017/01/02/crime-attack.html </a>. The idea behind the attack is that we can use repeated character patterns to determine which character pattern is most likely since the compression algorithm will shorten the text for repeats. The flag is crypto{CRIME_571ll_p4y5}. 
3. 
