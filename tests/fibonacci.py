x = 0
y = 1

counter = 0

while counter < 15:
    counter += 1
    x, y = y, x + y
    print x
