# -*- mode: python; -*-
# Execute this script using Bash script of the same name but without a file
# extension. Use ../pdbwrapper/pdbwrapper instead of pdb for debugging.

import os
import sys
import argparse

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
    args = parser.parse_args(sys.argv[1:])
    print("\n{}\nargs\n{}".format('-' * 80, args))


if __name__ == '__main__':
    sys.exit(0 if main() else 1)  # Return non-zero exit codes upon failure

# import pdb
# pdb.set_trace()
