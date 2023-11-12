f = open('./output.txt', 'r').read()
a = f.split('\n')
d = {}
start = ord('a')
txt = ''
for i,v in enumerate(a):
    if v not in d:
        d[v] = chr(start)
        start += 1
    txt += d[v]
print(txt)
# HTB{SIMPLE_SUBSTITUTION_CIPHER}

