# need to specify the order
s = 'write(0x14,&DAT_00100934,1); write(7,&DAT_00100936,1); write(0xc,&DAT_00100938,1); write(4,&DAT_0010093a,1); write(0x12,&DAT_0010093c,1); write(10,&DAT_00100938,1); write(0x1d,&DAT_00100934,1); write(0x15,&DAT_00100938,1); write(9,&DAT_0010093e,1); write(0x1c,&DAT_00100940,1); write(0xf,&DAT_00100942,1); write(0x10,&DAT_00100938,1); write(5,&DAT_00100944,1); write(0xe,&DAT_0010093c,1); write(8,&DAT_00100946,1); write(0x19,&DAT_00100948,1); write(0x11,&DAT_0010094a,1); write(6,&DAT_00100938,1); write(0x1a,&DAT_0010094c,1); write(3,&DAT_0010094a,1); write(0x16,&DAT_00100946,1); write(0xd,&DAT_0010094e,1); write(0x1b,&DAT_00100950,1); write(0xb,&DAT_00100952,1); write(0x13,&DAT_00100954,1); write(0x17,&DAT_00100956,1); write(0x18,&DAT_0010094e,1);'
a = ['e', 'D', '_', '0', '3', 'd', 'c', 't', 'w', '1', 'a', 'h', '7', '9', '8', 'i', 'R', 'b']
sa = s.split(';')
print(sa)
a2 = [s.split('(')[1].split(',')[0] for s in sa if s != '']
for i,v in enumerate(a2):
    if '0x' in v:
        a2[i] = int(v, 16)
    else:
        a2[i] = int(v, 10)

order = [s.split('09')[1].split(',')[0] for s in sa if s != '']
order = [int(i, 16) for i in order]
order = [(i - 52) // 2 for i in order]
print(a) # the dictionary
print(order)
print(a2)
print(len(a), len(order), len(a2))


write_vals = []
for i,v in enumerate(a2):
    write_vals.append((v, a[order[i]]))

print(write_vals)

# now sort on the secondy part of the tuple

sort_vals = sorted(write_vals, key = lambda x: x[0])
print(sort_vals)

ret = ''.join([i[1] for i in sort_vals])
print(len(ret))
print(ret)

#h0w_D1d_i_93t_h3Re_1b9a78ce