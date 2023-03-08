---
title: satellite
layout: post
---

<h2> Methodology </h2>
* Saw that it was networking problem, so I started up wireshark, typed in osmium, and went through all the options
* Looked through the packets that were captured in wireshark and saw that the flag was on one of them
* This also shows you that wireshark is used:
cat VXNlcm5hbWU6IHdpcmVzaGFyay1yb2NrcwpQYXNzd29yZDogc3RhcnQtc25pZmZpbmchCg== | base64 --decode
* flag: CTF{4efcc72090af28fd33a2118985541f92e793477f} 