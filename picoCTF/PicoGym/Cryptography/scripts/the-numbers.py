import string

k = [20, 8, 5, 14, 21, 13, 2, 5, 18, 19, 13, 1, 19, 15, 14]
a = string.ascii_uppercase
o = ""

for n in k:
    o += a[n - 1]

print(o)
