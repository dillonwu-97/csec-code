from pwn import *


sku = '💀 '
r = process('./deathnote')
r.sendafter(sku, "1")
r.sendafter(sku, "128") #size of 
r.sendafter(sku, "0") # page 
r.sendafter(sku, "aaa") # name

gdbscript='''
b _
'''
gdb.attach(r,gdbscript=gdbscript)



