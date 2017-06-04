python_condaenv_preamble
========================

[Parent README](../README.md)

Files:

- [python_condaenv_preamble](python_condaenv_preamble) -- The preamble wrapper that calls installs dependent packages into a conda environment and then calls the .py script.
- [example_condaenv_script](example_condaenv_script) -- An example conda-based wrapper script that calls a corresponding .py file

Rationale
=========

[python_condaenv_preamble](python_condaenv_preamble) is used to create
a new conda installation and within it a Python conda
environment.

This was done because of pip's inability to both compile and then
install binary packages such as matplotlib seamlessly. Binary python
packages such as matplotlib require several system dependent packages;
if you desire not to disturb the default system configuration, this is
an alternative.

See:
https://jakevdp.github.io/blog/2016/08/25/conda-myths-and-misconceptions/
for additional justification.

Usage
=====

Add the lines to a Bash script of the same name, sans the .py extension. For example:

    #!/bin/bash
    PYTHON_CONDAENV_REQUIRED_PACKAGES="import%20matplotlib|conda|matplotlib"
    . path_to_some_directory/python_condaenv_preamble "$0" "$@"

This example will install the matplotlib package using conda, and
verify it is installed by executing `import matplotlib`.

PYTHON_CONDAENV_REQUIRED_PACKAGES is a space-separated list of packages of the form:

    import_statement|installer|package_name

where installer can be one of "conda" or "pip".
