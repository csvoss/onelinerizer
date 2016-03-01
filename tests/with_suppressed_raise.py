class ContextManager(object):

    def __enter__(self):
        print "Entering"
        return "__enter__ value"

    def __exit__(self, type, value, traceback):
        print "Exiting"
        # Suppress the exception.
        return True


print "Before"
with ContextManager() as c:
    print "Before Raise"
    raise ValueError("Raise")

# This currently fails for reasons I don't quite understand.
# print "After"
