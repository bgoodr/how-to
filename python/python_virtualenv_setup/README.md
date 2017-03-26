python_virtualenv_setup
==========

[Parent README](../README.md)

Rationale
=========

[python_virtualenv_setup](python_virtualenv_setup) is used to create a new python virtualenv.

You must set the `PYTHON_LATEST` in your environment before executing
it, to point to the python executable you have built locally. This can
a actually be set to `/usr/bin/python` on systems that have a more
up-to-date Python (e.g., Ubuntu).

I could not just use `/usr/bin/python` on the RHEL systems since I am
not in control over the version of Python on those systems, but on the
Ubuntu systems I use I can control that via.

Usage
=====

Execute from the Bash prompt:

    PYTHON_LATEST=/the/path/to/your/latest/bin/python ./python_virtualenv_setup
