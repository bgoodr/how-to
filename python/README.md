python how-to examples
======================

See subdirectories as follows:

* [python_preamble_basic](python_preamble_basic/README.md) -- Example using a preamble script to execute a basic non-module python script.
* [python_preamble_directory_relative_module](python_preamble_directory_relative_module/README.md) -- Example using directory relative modules.
* [pdbwrapper](pdbwrapper/README.md) -- Wrapper to hack around problems with pdb and/or with Emacs.
* [python_virtualenv_setup](python_virtualenv_setup/README.md) -- Script to installa virtualenv.
* [python_virtualenv_preamble](python_virtualenv_preamble/README.md) -- Preamble script that installs packages into a virtualenv and runs a .py script.
* [.flake8](.flake8) -- Disable flake8 warnings

PEP8 Non-compliance
===================

I have disabled some of the warnings coming out of
[flake8](https://pypi.python.org/pypi/flake8) tool that the
[elpy](https://github.com/jorgenschaefer/elpy) package uses, because
they are excessive.

Find them disabled in [.flake8](.flake8).

Move that file aside and see them by opening up Emacs (previously
configured with [elpy](https://github.com/jorgenschaefer/elpy)) and
use `C-c C-n` to proceed to each one.
