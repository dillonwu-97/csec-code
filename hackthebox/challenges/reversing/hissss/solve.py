p = ['0'] * 12
p[0] = '0'
p[11] = '!'
p[1] = 'p'
p[4] = chr( 143 - ord(p[0]))
p[9] = chr(ord('n') - 1)
p[3] = chr(30 ^ ord(p[1]))
p[2] = chr(5610 // ord(p[3]))
p[10] = '3'
p[5] = chr( 166 - ord(p[10]) )
p[7] = 's'
p[6] = chr( 64 ^ ord(p[7]) )
p[8] = chr(ord(p[6]) + 46)


print(''.join(p))
# HTB{0p3n_s3sam3!}
