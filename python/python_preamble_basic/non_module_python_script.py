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
from datetime import datetime, timedelta
import calendar
import mmap
import cPickle as pickle
import pprint
import hashlib


# How to run the debugger at a particular area of code:
# import pdb
# pdb.set_trace()


def readlines(file):
    """Read all lines of a file."""
    with open(file, "r") as f:
        return f.readlines()


def readline_last(text_file):
    """An iterator to read from the last lines of a file.

    Example:

        for line in readline_last(accounting_file):
            line = line.rstrip()
            print 'line {}'.format(line)
    """
    file_size = os.stat(text_file).st_size
    if file_size == 0:
        return
    with open(text_file, "r+b") as f:
        map = None
        try:
            map = mmap.mmap(f.fileno(), 0)
            map.seek(0, os.SEEK_END)
            end = map.tell()
            if end == 0:
                return
            i = end - 1
            if map[i] == '\n':
                i -= 1
                if i < 0:
                    yield '\n'
                    return
            while i > 0:
                while i > 0 and map[i] != '\n':
                    i -= 1
                if map[i] == '\n':
                    i += 1
                map.seek(i)
                yield map.readline()
                i -= 1
                if i > 0 and map[i] == '\n':
                    i -= 1
        finally:
            if map:
                map.close()


def matchgroups(regexp, groupnum, item):
    """Return the group or groups for a given match, else return None.

    Be sure to either use parenthesis which are regular expression grouping operators:
      r'^(.*)$'
    or pass -1 to groupnum which means return the entire item.
    """
    m = re.search(regexp, item)
    if m:
        if groupnum is not None:
            if groupnum == -1:
                return item
            else:
                return m.group(groupnum)
        else:
            return m.groups()
        assert(False)
    return None


def matchalliter(items, match_re, groupnum):
    """Returns an iterator that matches all items in the regular expression given by match_re.

    Treats match_re and groupnum the same as matchgroups"""
    return itertools.ifilter(None, itertools.imap(functools.partial(matchgroups, match_re, groupnum), items))


def matchfirst(items, match_re, groupnum):
    """Find first matching item from items.

    Do not continue to evaluate items (short-circuiting).

    Reference: http://stackoverflow.com/a/43906867/257924"""
    return next(matchalliter(items, match_re, groupnum), None)


def matchfirstindex(indexes, items, match_re):
    """Return the index of indexes of the first item within items that matches the regular expression given by match_re."""
    return next(itertools.ifilter(lambda index: match_re.search(items[index]), indexes), None)


def demo_matchfirst():
    # Assume lines is constructed from some file using readlines above:
    lines = ["line {}".format(x) for x in range(0, 21)]
    lines[10] = "TIMESTAMP 2017-05-11 15:28"
    print 'lines {}'.format(lines)
    timestamp_re = r'^TIMESTAMP (.*)'
    timestamp = matchfirst(lines, timestamp_re, 1)
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


@contextmanager
def change_pwd(new_dir):
    """Temporarily change the current working directory to new_dir, restoring the original directory.

    with change_pwd(indir):
        # ... Do some processing with the current working directory being changed to indir here. ...
        pass
    """
    savedir = os.getcwd()
    os.chdir(new_dir)
    try:
        yield
    finally:
        os.chdir(savedir)


class Picklize:
    """Similar to Memoize in https://stackoverflow.com/a/1988826/257924 but pickles the result to disk."""

    def __init__(self, f):
        self.f = f

    def __call__(self, *args):
        sha1 = hashlib.sha1()
        sha1.update(str(args))
        hash = sha1.hexdigest()
        result_file = '/tmp/' + hash
        result = None
        if not os.path.exists(result_file):
            result = self.f(*args)
            with open(result_file, 'w') as f:
                pickle.dump(result, f)
        else:
            with open(result_file, 'r') as f:
                result = pickle.load(f)
        return result


@Picklize
def factorial(k):
    print("got k {}".format(k))
    if k < 2:
        return 1
    return k * factorial(k - 1)


# print("//////////")
# f1 = factorial(6)
# print("\n{}\nf1\n{}".format('-' * 80, f1))
# f2 = factorial(6)
# print("\n{}\nf2\n{}".format('-' * 80, f2))


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


def get_datetime_from_timestamp_milliseconds(milliseconds):
    """Convert a Unix timestamp in milliseconds since the epoch into a datetime object.

    Ref: http://stackoverflow.com/questions/748491/how-do-i-create-a-datetime-in-python-from-milliseconds/31625298#31625298
    """
    base_datetime = datetime(1970, 1, 1)
    delta = timedelta(0, 0, 0, milliseconds)
    return base_datetime + delta


def get_timestamp_from_datetime(dt, is_local_time=True):
    """Get an epoch timestamp from a UTC datetime.

    Ref: https://docs.python.org/2/library/calendar.html#calendar.timegm
         http://stackoverflow.com/a/8778548/257924"""
    if is_local_time:
        timestamp = time.mktime(dt.timetuple())  # DO NOT USE IT WITH UTC DATE
    else:
        timestamp = calendar.timegm(dt.timetuple())
    return timestamp


def demo_get_timestamp_from_datetime():
    xxx_dt1 = datetime.now()
    print 'xxx_dt1       {}'.format(xxx_dt1)
    xxx_string1 = '{}'.format(xxx_dt1.strftime('%Y-%m-%d %H:%M:%S'))
    print 'xxx_string1   {}'.format(xxx_string1)
    fmt = '%Y-%m-%d %H:%M:%S'
    xxx_dt2 = datetime.strptime(xxx_string1, fmt)
    print 'xxx_dt2       {}'.format(xxx_dt2)
    xxx_timestamp = get_timestamp_from_datetime(xxx_dt2, is_local_time=True)
    print 'xxx_timestamp {}'.format(xxx_timestamp)
    xxx_dt3 = datetime.fromtimestamp(xxx_timestamp)
    print 'xxx_dt3       {}'.format(xxx_dt3)
    assert xxx_dt2 == xxx_dt3


# demo_get_timestamp_from_datetime()


def example_time_calculations():
    """
    http://stackoverflow.com/questions/6999726/how-can-i-convert-a-datetime-object-to-milliseconds-since-epoch-unix-time-in-p?answertab=votes#comment36393216_6999787
    http://stackoverflow.com/questions/8777753/converting-datetime-date-to-utc-timestamp-in-python
    http://stackoverflow.com/a/8778548/257924
    """
    print
    start_time = "2017-05-09 21:53:55"
    format = "%Y-%m-%d %H:%M:%S"
    # dt0 will be a UTC date (not using pytz here so these are naive dates without timezones because my intent is to just do date subtraction to get timedeltas):
    dt0 = datetime.strptime(start_time, format)
    print 'dt0 {}'.format(dt0)
    print 'dt0.timetuple() {}'.format(dt0.timetuple())
    # 1494392035 should be a PDT localtime timestamp corresponding to 2017-05-09 21:53:55 in UTC:
    print 'datetime.fromtimestamp(1494392035)    {}'.format(datetime.fromtimestamp(1494392035))
    print 'datetime.utcfromtimestamp(1494392035) {}'.format(datetime.utcfromtimestamp(1494392035))
    timestamp = int((dt0 - datetime(1970, 1, 1)).total_seconds())
    print 'timestamp {}'.format(timestamp)
    print 'datetime.utcfromtimestamp(timestamp) {}'.format(datetime.utcfromtimestamp(timestamp))
    t0 = datetime.strptime("2017-05-11 06:20:00", format)
    t1 = datetime.strptime("2017-05-11 07:20:00", format)
    d = t1 - t0
    print int(d.total_seconds())
    # # Show how to get modification timestamp from file:
    # print 'os.stat("afile").st_mtime {:.06f}'.format(os.stat("afile").st_mtime)
    # print subprocess.check_output("find afile -printf \"%p %T@\\n\"; ls -ld afile", shell=True)
    # print 'datetime.fromtimestamp(os.stat("afile").st_mtime) {}'.format(datetime.fromtimestamp(os.stat("afile").st_mtime))


# Download and import pytz module:
import urllib2
tmpzip_path = "/tmp/pytz-because-python-does-not-include-it-when-it-really-should.zip"
if not os.path.isfile(tmpzip_path):
    downloads_f = urllib2.urlopen('https://pypi.python.org/pypi/pytz#downloads')
    lines = [line.rstrip() for line in downloads_f]
    zip_file = matchfirst(lines, r'<a href="(http[^"]*\.zip[^"]*)', 1)
    zip_download_f = urllib2.urlopen(zip_file)
    with open(tmpzip_path, "w") as tmp_zip_f:
        tmp_zip_f.write(zip_download_f.read())
if sys.path[0] != tmpzip_path:
    sys.path.insert(0, tmpzip_path)
import pytz


def example_pytz():
    """Example of pytz usage.

    This is to prove that the above insane dynamic download and import
    of the pytz module from the zip file actually works. I did that
    because I have to use several different Python 2.x versions where
    I cannot simply use pip as I would normally want to do.

    Ref: https://pypi.python.org/pypi/pytz

    """
    from pytz import timezone
    utc = pytz.utc
    print 'utc {}'.format(utc)
    print 'utc.zone {}'.format(utc.zone)
    eastern = timezone('US/Eastern')
    print 'eastern {}'.format(eastern)
    amsterdam = timezone('Europe/Amsterdam')
    print 'amsterdam {}'.format(amsterdam)
    fmt = '%Y-%m-%d %H:%M:%S %Z%z'
    loc_dt = eastern.localize(datetime(2002, 10, 27, 6, 0, 0))
    print 'loc_dt {}'.format(loc_dt)
    print 'loc_dt.strftime(fmt) {}'.format(loc_dt.strftime(fmt))
    ams_dt = loc_dt.astimezone(amsterdam)
    print 'ams_dt.strftime(fmt) {}'.format(ams_dt.strftime(fmt))
    utc_dt = datetime(2002, 10, 27, 6, 0, 0, tzinfo=utc)
    loc_dt = utc_dt.astimezone(eastern)
    print 'loc_dt.strftime(fmt) {}'.format(loc_dt.strftime(fmt))
    before = loc_dt - timedelta(minutes=10)
    print 'before.strftime(fmt) {}'.format(before.strftime(fmt))
    utc_dt = utc.localize(datetime.utcfromtimestamp(1143408899))
    print 'utc_dt.strftime(fmt) {}'.format(utc_dt.strftime(fmt))
    au_tz = timezone('Australia/Sydney')
    au_dt = utc_dt.astimezone(au_tz)
    print 'au_dt.strftime(fmt) {}'.format(au_dt.strftime(fmt))
    # pdt_tz = timezone('PDT')
    # print 'pdt_tz {}'.format(pdt_tz)
    uspac_tz = timezone('US/Pacific')
    print 'uspac_tz {}'.format(uspac_tz)
    print
    print "Choose a UTC date that we know will be PDT:"
    utc_dt = datetime(2002, 10, 27, 6, 0, 0, tzinfo=utc)
    print 'utc_dt {}'.format(utc_dt)
    uspac_dt = utc_dt.astimezone(uspac_tz)
    print 'uspac_dt.strftime(fmt) {}'.format(uspac_dt.strftime(fmt))
    print
    print "Choose a UTC date that we know will be PST:"
    utc_dt = datetime(2002, 12, 27, 6, 0, 0, tzinfo=utc)
    print 'utc_dt {}'.format(utc_dt)
    uspac_dt = utc_dt.astimezone(uspac_tz)
    print 'uspac_dt.strftime(fmt) {}'.format(uspac_dt.strftime(fmt))
    print
    print "Try strptime and strftime to include something similar to a timezone indicator:"
    # http://stackoverflow.com/a/14763408/257924 says:
    #   "You can format a timezone as a 3-letter abbreviation, but you can't parse it back from that"
    # So, see datetime_tz3_to_olson_tz below.
    fmt = '%Y-%m-%d %H:%M:%S'
    d = datetime.now(pytz.timezone("America/New_York"))
    dtz_string = d.strftime(fmt) + ' ' + "America/New_York"
    print 'dtz_string {}'.format(dtz_string)
    d_string, tz_string = dtz_string.rsplit(' ', 1)
    print 'd_string {}'.format(d_string)
    print 'tz_string {}'.format(tz_string)
    d2 = datetime.strptime(d_string, fmt)
    print 'd2 {}'.format(d2)
    tz2 = pytz.timezone(tz_string)
    print 'tz2 {}'.format(tz2)
    print 'dtz_string {}'.format(dtz_string)
    print d2.strftime(fmt) + ' ' + tz_string
    print
    print "How to convert from localtime to some other timezones: http://stackoverflow.com/a/13346065"
    pacific = pytz.timezone('US/Pacific')
    print 'pacific {}'.format(pacific)
    fmt = '%Y-%m-%d %H:%M:%S %Z%z'
    loc_dt = pacific.localize(datetime(2017, 05, 11, 21, 57, 0))
    print 'loc_dt {}'.format(loc_dt)
    print 'loc_dt.strftime(fmt) {}'.format(loc_dt.strftime(fmt))
    utc_dt = loc_dt.astimezone(pytz.UTC)
    print 'utc_dt {}'.format(utc_dt)
    print 'utc_dt.strftime(fmt) {}'.format(utc_dt.strftime(fmt))
    mountain = pytz.timezone('US/Mountain')
    print 'mountain {}'.format(mountain)
    mountain_dt = loc_dt.astimezone(mountain)
    print 'mountain_dt {}'.format(mountain_dt)
    print 'mountain_dt.strftime(fmt) {}'.format(mountain_dt.strftime(fmt))


def datetime_tz3_to_olson_tz():
    # http://stackoverflow.com/questions/7669938/get-the-olson-tz-name-for-the-local-timezone
    # was helpful: You HAVE to have a magic decoder ring:
    com_tzs = (com_tz for com_tz in pytz.common_timezones if re.search(r'^US', com_tz))
    fmt = '%Z'
    decoder = {}
    for com_tz in com_tzs:
        d = datetime.now(pytz.timezone(com_tz))
        short_tz = d.strftime(fmt)
        if short_tz[-2:] == 'DT' or short_tz[-2:] == 'ST':
            for x in ['DT', 'ST']:
                decoder[short_tz[0:-2] + x] = com_tz
    return decoder


def datetime_strptime_dwim(dt_str_with_3_letter_zone, default_3_letter_timezone="UTC"):
    """Parse a datetime string in the form of "YYYY-MM-DD HH:MM:SS ZZZ" where ZZZ is the three letter timezone into a datetime object.

    Ref: http://stackoverflow.com/questions/7669938/get-the-olson-tz-name-for-the-local-timezone"""
    dt_string, tm_string, tz_string = (None, None, None)  # <-- how to do this more elegantly?
    elems = dt_str_with_3_letter_zone.split(' ')
    if len(elems) == 3:
        dt_string, tm_string, tz_string = elems
    elif len(elems) == 2:
        dt_string, tm_string, tz_string = elems[0], elems[1], default_3_letter_timezone
    else:
        dt_string, tm_string, tz_string = elems[0], "00:00:00", default_3_letter_timezone
    decoder = datetime_tz3_to_olson_tz()
    if tz_string not in decoder:
        raise ValueError("ASSERTION FAILED: Unexpected timezone: {}".format(tz_string))
    olson_tz = pytz.timezone(decoder[tz_string])
    fmt = '%Y-%m-%d %H:%M:%S'
    dt = datetime.strptime("{} {}".format(dt_string, tm_string), fmt)
    loc_dt = olson_tz.localize(dt)
    dt2 = loc_dt.astimezone(olson_tz)
    # fmt = '%Y-%m-%d %H:%M:%S %Z%z'
    # print 'dt2.strftime(fmt) {}'.format(dt2.strftime(fmt))
    return dt2


# datetime_strptime_dwim("2017-05-11 20:44:00 PDT")
# datetime_strptime_dwim("2017-05-11")
# print datetime_strptime_dwim("2017-05-11 20:44:00 PDT")
# print datetime_tz3_to_olson_tz()
# example_pytz()


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
        prog=os.path.basename(os.path.splitext(sys.argv[0])[0]),  # Avoid showing the .py file extension in the usage help
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

    # Dump out environment in a form that can be source into Bash(-compatible) scripts:
    #
    #   Exclude the awful PWD environment variable that when reapplied
    #   causes great confusion with the pwd command who also sets PWD.
    #
    #   Exclude SHLVL which should be set by Bash shells.
    #
    excluded = set(["SHLVL", "PWD"])
    for k, v in os.environ.items():
        if "'" in v:
            delim = '"'
        else:
            delim = "'"
        if k in excluded:
            continue
        print "export {k}={delim}{v}{delim}".format(k=k, v=v, delim=delim)

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

    # --------------------------------------------------------------------------------
    # Using cPickle:
    # --------------------------------------------------------------------------------
    if True:
        data1 = {'a': [1, 2.0, 3, 4 + 6j],
                 'b': ('string', u'Unicode string'),
                 'c': None}
        selfref_list = [1, 2, 3]
        selfref_list.append(selfref_list)

        file = '/tmp/pickled'
        with open(file, "wb") as output:
            # Pickle dictionary using protocol 0.
            pickle.dump(data1, output)
            # Pickle the list using the highest protocol available.
            pickle.dump(selfref_list, output, -1)

        with open(file, "rb") as pkl_file:
            data1 = pickle.load(pkl_file)
            pprint.pprint(data1)
            data2 = pickle.load(pkl_file)
            pprint.pprint(data2)

    # --------------------------------------------------------------------------------
    # Custom exception classes: https://stackoverflow.com/a/6180231/257924
    # --------------------------------------------------------------------------------
    if True:
        class LineParseError(Exception):
            def __init__(self, message, line_num):
                self.message = message
                self.line_num = line_num

            def __str__(self):
                return repr("{}:{}".format(self.line_num, self.message))

        class FileLineParseError(Exception):
            def __init__(self, message, file, line_num):
                self.message = message
                self.file = file
                self.line_num = line_num

            def __str__(self):
                return repr("{}:{}:{}".format(self.file, self.line_num, self.message))

        def process_some_file(file):
            try:
                raise LineParseError("bla bla", 1002)
            except LineParseError as e:
                raise FileLineParseError(e.message, file, e.line_num)

        file = "thefile"
        try:
            process_some_file(file)
        except FileLineParseError as e:
            print("got error: {}".format(e))


if __name__ == '__main__':
    sys.exit(0 if main() else 1)  # Return non-zero exit codes upon failure
