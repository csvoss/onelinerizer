out = ''
for i in [1,2,3,4]:
    print i
    out += 'a'
    for j in [5,6,7,8]:
        print j
        out += 'b'
        continue
    else:
        print j
        out += 'c'
        if i == 2:
            continue
        elif i == 3:
            break
    out += 'd'
else:
    out += 'e'
print i, out
