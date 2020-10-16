'''
'A' ; 65
|           0x00400878      c645c15d       mov byte [local_3fh], 0x5d  ; ']' ; 93
|           0x0040087c      c645c24b       mov byte [local_3eh], 0x4b  ; 'K' ; 75
|           0x00400880      c645c372       mov byte [local_3dh], 0x72  ; 'r' ; 114
|           0x00400884      c645c43d       mov byte [local_3ch], 0x3d  ; '=' ; 61
|           0x00400888      c645c539       mov byte [local_3bh], 0x39  ; '9' ; 57
|           0x0040088c      c645c66b       mov byte [local_3ah], 0x6b  ; 'k' ; 107
|           0x00400890      c645c730       mov byte [local_39h], 0x30  ; '0' ; 48
|           0x00400894      c645c83d       mov byte [local_38h], 0x3d  ; '=' ; 61
|           0x00400898      c645c930       mov byte [local_37h], 0x30  ; '0' ; 48
|           0x0040089c      c645ca6f       mov byte [local_36h], 0x6f  ; 'o' ; 111
|           0x004008a0      c645cb30       mov byte [local_35h], 0x30  ; '0' ; 48
|           0x004008a4      c645cc3b       mov byte [local_34h], 0x3b  ; ';' ; 59
|           0x004008a8      c645cd6b       mov byte [local_33h], 0x6b  ; 'k' ; 107
|           0x004008ac      c645ce31       mov byte [local_32h], 0x31  ; '1' ; 49
|           0x004008b0      c645cf3f       mov byte [local_31h], 0x3f  ; '?' ; 63
|           0x004008b4      c645d06b       mov byte [local_30h], 0x6b  ; 'k' ; 107
|           0x004008b8      c645d138       mov byte [local_2fh], 0x38  ; '8' ; 56
|           0x004008bc      c645d231       mov byte [local_2eh], 0x31  ; '1' ; 49
|           0x004008c0      c645d374       mov byte [local_2dh], 0x74  ; 't' ; 116

'''

s = 'A]Kr=9k0=0o0;k1?k81t'
ret = ""
print(s, len(s))
for i in s:
    ret += chr(ord(i) ^ 9)
print(ret)
