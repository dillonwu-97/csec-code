keys = "1152 1344 1056 1968 1728 816 1648 784 1584 816 1728 1520 1840 1664 784 1632 1856 1520 1728 816 1632 1856 1520 784 1760 1840 1824 816 1584 1856 784 1776 1760 528 528 2000"

mykeys = "1552 1568 1584 1600"
mykeys_decoded = "abcd" # off by 16 so based on ascii table
# observation: 16 * 97 = 1552 (97 is ascii character for "a")

a = keys.split(" ")
a = "".join([chr(int(i)//16) for i in a])
print(a)
