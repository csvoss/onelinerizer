class ContextManager(object):

    def __enter__(self):
        print "Entering"

    def __exit__(self, type, value, traceback):
        print "Exiting"


print "Before"
with ContextManager() as c:
    print "In Body"
    raise ValueError("Raise")

print "After"
