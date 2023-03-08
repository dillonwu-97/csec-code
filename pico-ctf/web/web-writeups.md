---
title: web-exploitation
tags: web exploit
---

### Insp3ct0r
Inspect the first page to find the first part of the flag, which is picoCTF{tru3\_d3
Go the the source of the css, which is mycss.css to find the second part: t3ct1ve\_0r\_ju5t
Go the the source of the javascript, which is myjs.js to find the third part of the flag:  \_lucky?f10be399}

### logon
Pretty simple. Intercept the request with Burp, and then change admin=false to admin=true and refresh the page.
picoCTF{th3\_c0nsp1r4cy\_l1v3s\_6edb3f5f}

### where are the robots
Go to robots.txt. 
picoCTF{ca1cu1at1ng\_Mach1n3s\_8028f}

### dont-use-client-side
Look at the page source to see the flag, which is split up into several parts. The joined flag is 
picoCTF{no\_clients\_plz\_7723ce}

### web gauntlet
1. SQL injection using the syntax SELECT * FROM users WHERE username='admin' AND password='admin'. The filter.php file also states that we cannot use OR in our filter statement.
The injection should be  
username: admin
password: 


### picobrowser
Intercept the request using Burp-Suite and then change the User-Agent to picobrowser. 
picoCTF{p1c0\_s3cr3t\_ag3nt\_51414fa7}

### Client-side again
First, niceify the JS code.  
Observations about the code:  
1) There is an array called \_0x5a46 which gets shifted so that the value at \_0x5a46[0] is getElementById, and the value at \_0x5a46[9] is "Incorrect Password".
2) The function \_0x4b5b takes in two arguments, but if there is only one argument passed, then it is the level parameter.
The joined values for the flag are picoCTF{not\_this\_again\_50a029}

### Irish-Name-Repo 1
Simple SQL injection using   
username: admin
password: ' or 1=1;--
The flag is picoCTF{s0m3\_SQL\_fb3fe2ad}

### Irish-Name-Repo 2
SQL injection that involves ignoring password: 
username: admin';--
password: admin
The flag is picoCTF{m0R3\_SQL\_plz\_c34df170}

### Irish-Name-Repo 3
This is also pretty simple. It's the same as Irish-Name-Repo 1 except the letters are shifted by 13 so the exploit is:  
password: ' be 1=1;--
The flag is picoCTF{3v3n\_m0r3\_SQL\_4424e7af}

### JaWT Scratchpad
For this challenge, I tried doing the "none" algorithm exploit, but it didn't work. The "none" algorithm involves creating
a cookie which consists of the data {"typ": "JWT","alg": "none"}{"user": "admin"} base64 encoded ignoring trailing = signs. Unfortunately,
this strategy does not work.   
  
It turns out that I actually need to crack the key used for the JWT token generation using John the Ripper. The post here shows 
in detail how to use john or hashcat to crack JWT tokens: <a href="https://github.com/magnumripper/JohnTheRipper">
https://github.com/magnumripper/JohnTheRipper </a>.  
Basically, I need to get the rockyou.txt password list, and then use john to crack the hash. The exact command is:  
../run/john /tmp/jawt/crackme.txt --wordlist=/tmp/jawt/rockyou.txt  
where the crackme.txt file contains the full JWT token. Afterwards, construct a new token with "admin" in the user field and modify the cookie using Burp. Then, reload the page
and you have the flag which is picoCTF{jawt\_was\_just\_what\_you\_thought\_44c752f5}  
Note: modifying document.cookie on chrome is weird: <a href="https://stackoverflow.com/questions/16975941/modify-document-cookie-in-chrome-console-not-working"> https://stackoverflow.com/questions/16975941/modify-document-cookie-in-chrome-console-not-working </a>

### Scavenger Hunt
index.html: picoCTF{t
mycss.css:  h4ts_4_l0
robots.txt: t_0f_pl4c
.htaccess: 3s_2_lO0k
.DS_Store: \_7a46d25d}
picoCTF{th4ts_4_l0t_0f_pl4c3s_2_lO0k_7a46d25d}
