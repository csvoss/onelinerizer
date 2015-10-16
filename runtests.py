import unittest
import os
import sys
from StringIO import StringIO
from main import to_one_line

TEST_DIRECTORY = 'tests'

DEBUG = False

class TestOneLine(unittest.TestCase):
    def runTest(self):
        pass

def make_test(filename):
    """Return a function that verifies that the file and its onelined version
    both output the same."""

    def new_test(self):
        with open(filename, 'r') as fi:
            self.longMessage = True
            original = fi.read().strip()
            onelined = to_one_line(original)
            self.assertEqual(capture_exec(original),
                             capture_exec(onelined),
                             msg="\n\nOnelined: "+onelined)
    return new_test

class FakeStdin(object):
    """Sometimes tests use raw_input; this feeds those deterministically."""
    def __init__(self):
        self.counter = 0
    def readline(self):
        self.counter += 1
        return str(self.counter)

def capture_exec(code_string):
    """Run the code with FakeStdin as stdin, return its stdout."""
    ## TODO: Seed the RNG.
    new_stdout = StringIO()
    old_stdout = sys.stdout
    old_stdin = sys.stdin
    sys.stdout = new_stdout
    sys.stdin = FakeStdin()
    namespace = {}
    try:
        exec code_string in namespace
    except Exception as e:
        import traceback
        exc = traceback.format_exc()
        if DEBUG:
            old_stdout.write("\nFYI: test threw error %s\n" % str(type(e)(code_string + ', ' + exc)))
        new_stdout.write("Error thrown.")
    sys.stdout = old_stdout
    sys.stdin = old_stdin
    return new_stdout.getvalue()

## Monkey-patch 
for subdir, dirs, files in os.walk(TEST_DIRECTORY):
    for filename in files:
        root, ext = os.path.splitext(filename)
        if ext == '.py' and 'unimplemented' not in subdir:
            setattr(TestOneLine,
                    'test_%s' % root,
                    make_test(os.path.join(subdir, filename)))

if __name__ == '__main__':
    unittest.main()

