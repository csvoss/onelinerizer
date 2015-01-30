x = 5
for i in range(5):
    x = x + i
print x

# inner loop takes in d, returns a modified d?
# list: a list of i
# function: takes in i, d; spits out d
# for loop: takes in d, spits out d
# reduce: function, sequence, initial
# (lambda d.x: (lambda d: print(d.x))(reduce((lambda d, i: (lambda d.x: d)(d.x+i)), range(5), d)))(5)
