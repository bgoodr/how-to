# -*- mode: python; -*-
# Execute this script using Bash script of the same name but without a file
# extension. Use ../pdbwrapper/pdbwrapper instead of pdb for debugging.

import os
import sys
import argparse
import re
import time
from contextlib import contextmanager
import subprocess
from inspect import currentframe, getframeinfo
import itertools
import functools


def readlines(file):
    with open(file, "r") as f:
        return f.readlines()


def matchgroups(regexp, groupnum, line):
    m = re.search(regexp, line)
    if m:
        return m.group(groupnum) if groupnum is not None else m.groups()
    return None


def firstof(lines, match_re, groupnum):
    """Find result from the first call to pred of items.

    Do not continue to evaluate items (short-circuiting).

    Reference: http://stackoverflow.com/a/43906867/257924"""
    return next(itertools.ifilter(None, itertools.imap(functools.partial(matchgroups, match_re, groupnum), lines)), None)


def demo_firstof():
    # Assume lines is constructed from some file using readlines above:
    lines = ["line {}".format(x) for x in range(0, 21)]
    lines[10] = "TIMESTAMP 2017-05-11 15:28"
    print 'lines {}'.format(lines)
    timestamp_re = r'^TIMESTAMP (.*)'
    timestamp = firstof(lines, timestamp_re, 1)
    print 'timestamp {}'.format(timestamp)


# Example of contextmanager (http://tinyurl.com/llogvwu):
#
#   with time_print("processes"):
#       [doproc() for _ in range(500)]
#
@contextmanager
def time_print(task_name):
    t = time.time()
    try:
        yield
    finally:
        print task_name, "took", time.time() - t, "seconds."


# TODO: Moving the print_file_line function into debug_utils.py, and
# importing it, and calling it from this function does not work:
#
#   from debug_utils import print_file_line
#
# it emits :
#   debug_utils.py:263: got ['a', 'b', 'c']
#
# So for now just inline it everywhere I need it (reference http://stackoverflow.com/a/20372465/257924 ):
def print_file_line(*args):
    """Print args in grep-like formatted output.

    Print in format like grep -n -H would emit for compatibility
    with other tools that expect it (e.g., Emacs grep and compile
    mode buffers).
    """
    cf = currentframe()
    print "{}:{}: {}".format(getframeinfo(cf).filename, cf.f_back.f_lineno, " ".join([str(x) for x in args]))


def demo_print_file_line():
    """Demonstrate print_file_line."""
    print "got it"
    # print_file_line("got here")
    print "got it"
    print_file_line("got", ["a", "b", "c"])
    print "got it"
    print_file_line("got", ["a", "b", "c", "d"])


description = r"""
the_name_of_script_goes_here -- Short description line goes here

Multi-line description goes here.

Multi-line description goes here.

Multi-line description goes here.
"""


def main():
    """
    Main function
    """
    # Parse command-line arguments:
    #    https://docs.python.org/2/howto/argparse.html
    parser = argparse.ArgumentParser(
        description=description,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-theint", type=int,
                        help="some integer")

    # Warning: because of this nargs='+' item below, this is valid:
    #
    #     non_module_python_script.py -runmod one two -simplearg bar lonely
    #
    # but this is invalid:
    #
    #     non_module_python_script.py -simplearg bar -runmod one two lonely
    #     usage: non_module_python_script.py [-h] [-theint THEINT]
    #            [-runmod RUNMOD [RUNMOD ...]]
    #            [-simplearg SIMPLEARG] [-v] lonearg
    #     non_module_python_script.py: error: too few arguments
    #
    parser.add_argument('-runmod', nargs='+',
                        help='runner and its arguments')
    parser.add_argument('-simplearg', help='a simple arg')

    # Demonstrate a mutually exclusive group:
    action = parser.add_mutually_exclusive_group(required=False)
    action.add_argument('--option1', action='store_true', help='The first option')
    action.add_argument('--option2', action='store_true', help='The second option')
    action.add_argument('--option3', action='store_true', help='The third option')

    parser.add_argument('lonearg', help='a lone arg')
    # -v is an example of an argument that does not take a value
    # (http://stackoverflow.com/a/5271692/257924):
    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                        action="store_true")
    args = parser.parse_args(sys.argv[1:])

    # Call a function that demonstrates print_file_line:
    demo_print_file_line()

    print 'args.runmod {0}'.format(args.runmod)
    print 'args.simplearg {0}'.format(args.simplearg)
    print 'args.lonearg {0}'.format(args.lonearg)
    print 'args.theint {0}'.format(args.theint)
    print 'args.option1 {0}'.format(args.option1)
    print 'args.option2 {0}'.format(args.option2)
    print 'args.option3 {0}'.format(args.option3)

    # --------------------------------------------------------------------------------
    # Lists:
    # --------------------------------------------------------------------------------
    thelist = ["foo", "bar"]
    thejoinedstring = " ".join(thelist)
    print "thejoinedstring<" + thejoinedstring + ">"

    # --------------------------------------------------------------------------------
    # Environment variables:
    # --------------------------------------------------------------------------------

    env = "SOME_VAR||unset"
    # env = "SOME_VAR|var"
    vals = env.split('|')
    print 'vals' + str(vals)
    if len(vals) == 3:
        var = vals[0]
        print "Unsetting environment variable:", var
        if var in os.environ:
            del os.environ[var]
    else:
        var, val = vals
        print "Setting environment variable: {0}={1}".format(var, val)
        os.environ[var] = val

    print 'Left aligned example:  x{0:<20}x'.format('foo')
    print 'Right aligned example: x{0:>20}x'.format('foo')
    print 'Floating point format: {:.6f}'.format(12.1234)

    # --------------------------------------------------------------------------------
    # Reading from subprocesses:
    # --------------------------------------------------------------------------------

    # For more advanced methods that are Unix specific, See:
    #
    #  1. handling stdout and stderr from Popen:
    #     http://stackoverflow.com/a/7730201
    #  2. http://stackoverflow.com/a/17698359/257924
    #
    # Demonstrate that multiple shell commands can be included in the cmd:
    cmd = 'export THE_ENV_VAR=the_env_var_value; ls -ld /etc /etc/does_not_exist; echo THE_ENV_VAR==$THE_ENV_VAR'
    #
    #
    # This does not work: it prints each character in the stdout_line,
    # not each line:
    #
    if False:
        print 'Example: Reading stdout and stderr from a process based upon http://stackoverflow.com/a/17698359/257924'
        p = subprocess.Popen(cmd,
                             shell=True,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        for stdout_line in stdout:
            print 'stdout_line=="{}"'.format(stdout_line)
        for stderr_line in stderr:
            print 'stderr_line=="{}"'.format(stderr_line)
    #
    # This variation works.
    #   See http://stackoverflow.com/a/17698359/257924
    #
    if True:
        print 'Example: Reading stdout and stderr from a process based upon http://stackoverflow.com/a/17698359/257924'
        # shell=True as otherwise "ls ..." raises exception of "no such file
        # or directory":
        p = subprocess.Popen(cmd,
                             shell=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             bufsize=1)
        #
        # Read all of stdout:
        #
        with p.stdout:
            for stdout_line in iter(p.stdout.readline, b''):
                print 'stdout_line=="{}"'.format(stdout_line)
        #
        # Read all of stderr:
        #
        with p.stderr:
            for stderr_line in iter(p.stderr.readline, b''):
                print 'stderr_line=="{}"'.format(stderr_line)
        p.wait()  # wait for the subprocess to exit

        print "Example: Simplified Reading combined stdout and stderr from a process."
        p = subprocess.Popen(cmd,
                             shell=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT,
                             bufsize=1)

        #
        # Read all of stdout (which should contain stderr due to the stderr
        # directive above):
        #
        with p.stdout:
            for line in iter(p.stdout.readline, b''):
                line = line.rstrip()
                print line
        p.wait()  # wait for the subprocess to exit and set return code
        print "exit code: {}".format(p.returncode)

    # --------------------------------------------------------------------------------
    # Reading/writing from files and matching on regular expressions:
    # --------------------------------------------------------------------------------

    if True:
        print "Example: Reading a file and matching on regular expressions and subgroups:"
        in_file = "/etc/issue"
        with open(in_file, 'r') as f:
            for line in f:
                line = line.rstrip()
                m = re.search("release *([0-9.]+)", line)
                if m:
                    release_num = m.group(1)
                    print "release_num == <{}>".format(release_num)

        print "Example: Reading a file and searching/replacing on a regular expression:"
        with open(in_file, 'r') as f:
            for line in f:
                line = line.rstrip()
                line = re.sub(r'release', '<REPLACEMENT>', line)
                print line

        print "Example: Writing a file and searching/replacing on a regular expression"
        that_file = "/tmp/somefile.for.pythonTemplate"
        queue = ["testing", "one", "two", "three"]
        with open(that_file, 'w') as f:
            for line in queue:
                f.write(line + "\n")

    # --------------------------------------------------------------------------------
    # Context managers:
    # --------------------------------------------------------------------------------

    if True:
        with time_print("something to do"):
            print 'sleeping ...'
            time.sleep(1)

    # --------------------------------------------------------------------------------
    # Working with dictionaries:
    # --------------------------------------------------------------------------------

    if True:
        # Formatting dictionary using lambda:
        line_style = {"fill": "none", "fill-capacity": 1}
        print ";".join(map(
            lambda (k, v): "{}:{}".format(k, str(v)),
            line_style.iteritems()))

    # --------------------------------------------------------------------------------
    # Try/except clauses:
    # --------------------------------------------------------------------------------

    if True:
        try:
            raise argparse.ArgumentTypeError('{} was not set in the environment.'.format("THE_ENV_VAR"))
        except argparse.ArgumentTypeError, e:
            # raise Exception, "%s [%d]" % (e.strerror, e.errno)
            print "The exception {}".format(e)


if __name__ == '__main__':
    main()

demo_firstof()
