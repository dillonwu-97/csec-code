from random import randint
from secrets import flag, r

pubkey = Matrix(ZZ, [
    [47, -77, -85],
    [-49, 78, 50],
    [57, -78, 99]
])

# Some r difference 
# [ord(c), random integer less than 100, random integer less than 100 ]
# multiplied by the matrix [1*3] * [3*3] -> [1*3]
# some common r added 

# Ideas include using a z solver maybe?
[a, b, c]      [d, e, f
                g, h, i
                j, k, l]

[a * d + b * g + c * j,  a * e + b * h + c * k,  a * f + b * i + c * j]

for c in flag:
    v = vector([ord(c), randint(0, 100), randint(0, 100)]) * pubkey + r
    print(v)


(-981, 1395, -1668)
