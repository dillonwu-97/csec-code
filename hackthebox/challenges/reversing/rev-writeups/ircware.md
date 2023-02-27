---
title: ircware
description: Reverse engineering challenge that I thought was pretty difficult
tags: reversing, ghidra
---

I thought this was a pretty difficult reversing challenge. There were several mistakes I made for this challenge. The first mistake I made was that I thought the random function was used as some sort of gateway mechanism and that I had to guess the random value or else I couldn't continue to debug the rest of the code, but I was incorrect. The random function was just used to create a random username. In actuality, the reason the code resulted in "EXCEPTION ABORT" was because I needed to set up a localhost connection on port 8000. This led to my second mistake. I saw that it was making a connection somewhere, but I could not identify the ip address or port it was trying to connect to. After some more careful analysis, I saw that it was trying to connect to 0x100007f which converted to ip format is 127.0.0.1, and the port value was 0x401f (which because of little endian format) is actually 0x1f40 -> 8000. Third, I did not realize that it was reading commands of a specific format; specifically irc commands like PING. This meant that I had to enter commands like PRIVMSG #secret ":@pass ASS3MBLY", "PRIVMSG #secret :@flag", and "PING :". Finally, I did not look at the code carefully enough. The password required to get the flag was not RJJ3DSCP. Instead it was ASS3MBLY, which is the conversion of RJJ3DSCP in ROT9. There were assembly instructions showing that it subtracted 9 from the character input by the user this at the bottom of the ghidra compilation.

<img src = "/csec-writeups/hackthebox/htb-reversing/ircware-1.png" />

I also learned that starti is used to jump immediately into the very first instruction of the program. Additionally, info file can be used to find the entry point of the program.

<img src = "/csec-writeups/hackthebox/htb-reversing/ircware-2.png" />

The flag is: HTB{m1N1m411st1C_fL4g_pR0v1d3r_b0T}



