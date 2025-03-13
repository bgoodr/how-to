python_condaenv_preamble
========================

WARNING: Do not use this anymore at all. This was built before
Anaconda decided to bait-and-switch us all by changing their license
to require purchasing. Do not use it even for personal work because
eventually you will make the mistake of forgetting about that bait and
switch tactic, and then your usage will leak back into contexts that
are in violation of their license.

[Parent README](../README.md)

Files:

- [python_condaenv_preamble](python_condaenv_preamble) -- The preamble wrapper that calls installs dependent packages into a conda environment and then calls the .py script.
- [example_condaenv_script](example_condaenv_script) -- An example conda-based wrapper script that calls a corresponding .py file

See also [python_matplotlib](../python_matplotlib/README.md) for more indepth matplotlib-using script that leverages this preamble script.

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

Read the comments at the top of the [python_condaenv_preamble](python_condaenv_preamble) script.
