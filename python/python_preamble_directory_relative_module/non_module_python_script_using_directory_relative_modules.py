# -*- mode: python; -*-
# Execute this script using Bash script of the same name but without a file
# extension. Use ../pdbwrapper/pdbwrapper instead of pdb for debugging.

import sys

# sys.path hack for relative module paths:
import os
my_dir = None
try:
    my_dir = os.path.dirname(os.path.abspath(__file__))
except:
    # For when using C-c C-c from Emacs elpy package, to avoid messiness with setting PYTHONPATH:
    my_dir = os.getcwd()
sys.path.insert(0, os.path.join(my_dir, "my_python_module_dir"))
from my_module import do_something_important

do_something_important("some value")
