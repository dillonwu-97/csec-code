s = "}a:Vh|}a:g}8j=}89gV<p<}:dV8<Vg9}V<9V<:j|{:"
ret = ""
for i in s:
	ret += chr(ord(i) ^ 9)

print("CHTB{" + ret + "}")