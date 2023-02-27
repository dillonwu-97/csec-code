---
title: xorxorxor
description: Easy xor challenge
tags: xor, crypto
---

The solution to this challenge was pretty easy. I knew that the first four characters in the flag are "{HTB". The key length is 4 bytes, and it is used to encode the rest of the flag. I xored each of the ascii values in "{HTB" with the first four ascii values of the output.txt to get the key which consisted of the numbers [91, 30, 180, 154]. I used these numbers to get the rest of the flag which was HTB{rep34t3d\_x0r\_n0t\_s0\_s3cur3}. 