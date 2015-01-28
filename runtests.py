import unittest
import os
import sys
from StringIO import StringIO
from main import to_one_line

TEST_DIRECTORY = 'tests'

class TestOneLine(unittest.TestCase):
    def runTest(self):
        pass

def make_test(filename):
    def new_test(self):
        with open(filename, 'r') as fi:
            self.longMessage = True
            original = fi.read().strip()
            onelined = to_one_line(original)
            self.assertEqual(capture_exec(original),
                             capture_exec(onelined),
                             msg="Onelined: "+onelined)
    return new_test

def capture_exec(code_string):
    new_stdout = StringIO()
    old_stdout = sys.stdout
    sys.stdout = new_stdout
    try:
        exec code_string
    except Exception as e:
        raise type(e)(e.message + ', with code: ' + code_string)
    sys.stdout = old_stdout

for subdir, dirs, files in os.walk(TEST_DIRECTORY):
    for filename in files:
        setattr(TestOneLine,
                'test_%s' % filename.split('.')[0],
                make_test(os.path.join(subdir, filename)))

if __name__ == '__main__':
    unittest.main()

