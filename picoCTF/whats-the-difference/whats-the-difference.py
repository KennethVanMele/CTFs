kitters = open("kitters.jpg", "rb").read()
cattos = open("cattos.jpg", "rb").read()
dif = ""

for a, b in zip(kitters, cattos):
    if a != n:
        diff += b

print
diff
