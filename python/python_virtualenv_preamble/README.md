python_virtualenv_preamble
=====================

[Parent README](../README.md)

Files:

- [python_virtualenv_preamble](python_virtualenv_preamble) -- The preamble wrapper that calls installs dependent packages into a virtualenv and then calls the .py script.


Usage
=====

Add the lines to a Bash script of the same name, sans the .py extension

    #!/bin/bash
    PYTHON_VIRTUAL_ENV_REQUIRED_PACKAGES="import%20svgutils.transform|svgutils"
    . path_to_some_directory/python_virtualenv_preamble "$0" "$@"

This example will install the svgutils package using pip, and verify it is installed by executing `import svgutils.transform`.
