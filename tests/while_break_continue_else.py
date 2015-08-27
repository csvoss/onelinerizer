out = ''
f = True
while True:
    out += 'a'
    g = True
    while g:
        g = False
        out += 'b'
        continue
    else:
        out += 'c'
        if f:
            f = False
            continue
        else:
            break
    out += 'd'
else:
    out += 'e'
print out
