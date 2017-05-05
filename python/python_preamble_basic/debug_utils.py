# http://stackoverflow.com/a/20372465/257924
from inspect import currentframe, getframeinfo


def print_file_line(*args):
    """Print args in grep-like formatted output.

    Print in format like grep -n -H would emit for compatibility
    with other tools that expect it (e.g., Emacs grep and compile
    mode buffers).
    """
    cf = currentframe()
    print "{}:{}: {}".format(getframeinfo(cf.f_back).filename, cf.f_back.f_lineno, " ".join([str(x) for x in args]))

