print [i for i in range(5) if i%2==0]
print [i for j in range(5) for i in range(j)]
print [i for j in range(5) if j%2==0 for i in range(j) if i%2==0]
