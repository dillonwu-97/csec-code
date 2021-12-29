from z3 import *

a = Bool("a")
b = Bool("b")
c = Bool("c")
d = Bool("d")
e = Bool("e")
f = Bool("f")
g = Bool("g")
h = Bool("h")
i = Bool("i")
j = Bool("j")

ab = Not(Or([a, Not(b)]))
cd = Or([d, Not(c)])
ef = Or([e, Not(f)])
gh = Not(Or([g,h]))
hi = Xor(h,i)
ij = And([i,j])

cdef = Not(Or([cd,ef]))
abcdef = And([ab,cdef])

ghi = And([gh, hi])
ghij = And([ghi, ij])

abcdefghij = And([abcdef, ghij])


s = Solver()
s.add(abcdefghij)
s.check()
m = s.model()
a = sorted([(d, m[d]) for d in m], key = lambda x: str(x[0]))
ret = "CTF{"
for i in a:
	if i[1] == True:
		print(i[0], 1)
		ret += str(i[0])
	else:
		print(i[0], 0)
ret += "}"
print(ret.upper())