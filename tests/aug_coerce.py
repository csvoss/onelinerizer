class C:
    def __coerce__(self, other):
        return 2, 2
o = C()
o += C()
print o
