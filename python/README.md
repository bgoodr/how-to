python how-to examples
======================

See subdirectories as follows:

* [.flake8](.flake8) -- Disable flake8 warnings
* [pdbwrapper](pdbwrapper/README.md) -- Wrapper to hack around problems with pdb and/or with Emacs.
* [python_condaenv_preamble](python_condaenv_preamble/README.md) -- Preamble script that installs packages into a conda-based environment and runs a .py script.
* [python_matplotlib](python_matplotlib/README.md) -- Demonstrate using matplotlib which use the [python_condaenv_preamble](python_condaenv_preamble) script
* [python_preamble_basic](python_preamble_basic/README.md) -- Example using a preamble script to execute a basic non-module python script.
* [python_preamble_directory_relative_module](python_preamble_directory_relative_module/README.md) -- Example using directory relative modules.
* [python_virtualenv_preamble](python_virtualenv_preamble/README.md) -- Preamble script that installs packages into a virtualenv and runs a .py script.
* [python_virtualenv_setup](python_virtualenv_setup/README.md) -- Script to install a virtualenv.

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

References
==========

* https://gist.github.com/twolfson/7636887
