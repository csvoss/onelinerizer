import argparse
import sys

from .onelinerizer import onelinerize

def main():
    usage = ['onelinerizer --help',
             'onelinerizer [--debug] [infile.py [outfile.py]]',
            ]
    parser = argparse.ArgumentParser(usage='\n       '.join(usage),
        description=("if infile is given and outfile is not, outfile will be "
                     "infile_ol.py"))
    parser.add_argument('infile', nargs='?')
    parser.add_argument('outfile', nargs='?')
    parser.add_argument('--debug', action='store_true')
    args = parser.parse_args()
    original = None
    if args.infile is None:
        # I have gotten no arguments. Look at sys.stdin
        original = sys.stdin.read()
        outfilename = None
    elif args.outfile is None:
        # I have gotten one argument. If there's something to read from
        # sys.stdin, read from there.
        if args.infile.endswith('.py'):
            outfilename = '_ol.py'.join(args.infile.rsplit(".py", 1))
        else:
            outfilename = args.infile + '_ol.py'
    else:
        outfilename = args.outfile

    if original is None:
        infile = open(args.infile)
        original = infile.read().strip()
        infile.close()
    onelinerized = onelinerize(original)
    if outfilename is None:
        print onelinerized
    else:
        outfi = open(outfilename, 'w')
        outfi.write(onelinerized + '\n')
        outfi.close()

    if args.debug:
        if outfilename is None:
            # redirect to sys.stderr if I'm writing outfile to sys.stdout
            sys.stdout = sys.stderr
        print '--- ORIGINAL ---------------------------------'
        print original
        print '----------------------------------------------'
        scope = {}
        try:
            exec(original, scope)
        except Exception as e:
            traceback.print_exc(e)
        print '--- ONELINERIZED -----------------------------'
        print onelinerized
        print '----------------------------------------------'
        scope = {}
        try:
            exec(onelinerized, scope)
        except Exception as e:
            traceback.print_exc(e)

if __name__ == '__main__':
    main()
