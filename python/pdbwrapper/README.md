pdbwrapper
==========

[Parent README](../README.md)

Before adding the [pdbwrapper](pdbwrapper) script, I had this
awkwardness at the top of all of my non-module .py files:

    #!/bin/sh
    # -*- mode: python; coding: utf-8 -*-
    """:"
    export PYTHONPATH="$(dirname $0)/python:${PYTHONPATH}"
    exec /usr/bin/env python -u "$0" "$@"
    " """
    
    # To execute under the python debugger:
    #   1. Comment out the above preamble so that pdb can parse it.
    #   2. M-x pdb
    #   3. pdbwrapper name_of_this_script.py args...
    #   4. fix bugs.
    #   5. Don't forget to uncomment out the lines in step 1.
   
Instead I can now use [pdbwrapper](pdbwrapper) when invoking pdb (`M-x pdb`
from within Emacs).

Here we use "name_of_this_script" and NOT "name_of_this_script.py" so
we can then exec the preamble with the PYTHON_PREAMBLE_EXTRA_ARGS
option:

    pdbwrapper name_of_this_script args...

If you forget and put in the `.py` on the filename, the
[pdbwrapper](pdbwrapper) will error out.

Unfortunately, the RHEL (Red Hat Enterprise Licensing) I work lack the
/usr/bin/pdb executable. But it seems that, on Ubuntu, /usr/bin/pdb is
the same as the pdb.py file in the Python distribution. So we hack around
that bug by inject `-m pdb` into the command line when we invoke the
script.

Note: Emacs's pdb command (actually the code it calls which is
`gud-common-init`) has a bug in that it splits only on double quotes
not on single quotes. You can see that via this code:

    for arg in "$@"
    do
      echo "arg==\"${arg}\""
    done

So hack around that by using double-quotes around each option that
contains spaces when you invoke the [pdbwrapper](pdbwrapper) script.


Bash command line usage
=======================

Example bash session:


    $ cd ../python_preamble_directory_relative_module/
    $ ../pdbwrapper/pdbwrapper non_module_python_script_using_directory_relative_modules
    > <SNIP>/python_preamble_directory_relative_module/non_module_python_script_using_directory_relative_modules.py(5)<module>()
    -> import sys
    (Pdb) n
    > <SNIP>/python_preamble_directory_relative_module/non_module_python_script_using_directory_relative_modules.py(8)<module>()
    -> import os
    (Pdb) n
    > <SNIP>/python_preamble_directory_relative_module/non_module_python_script_using_directory_relative_modules.py(9)<module>()
    -> my_dir = None
    (Pdb)    <CTRL-d>
    $ 


Emacs pdb usage
===============

Open up the ../python_preamble_directory_relative_module/ directory in Emacs.

Execute:

   M-x pdb
   ../pdbwrapper/pdbwrapper non_module_python_script_using_directory_relative_modules

You should see a `*gud-non_module_python_script_using_directory_relative_modules*` buffer where you can proceed to set breakpoints:

    Current directory is ~/bgoodr/how-to/python/python_preamble_directory_relative_module/
    > /home/brentg/bgoodr/how-to/python/python_preamble_directory_relative_module/non_module_python_script_using_directory_relative_modules.py(5)<module>()
    -> import sys
    (Pdb)
