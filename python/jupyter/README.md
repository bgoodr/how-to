Jupyter
=======

[Parent README](../README.md)

jupyter_once.sh
---------------

[jupyter_once.sh](jupyter_once.sh) is a script that is intended to
launch a single local Jupyter server on your local machine, so as to
prevent launching multiple servers. Usually, when you are doing local
development, you want only one.

Execute from the Bash prompt:

    ./jupyter_once.sh

To kill off all jupyter server processes, use the `-k` option:

    ./jupyter_once.sh -k

Using the `jupyter_once.sh` script on this directory, you can click on
the one of the notebook files, `*.ipynb`, to open it on the Jupyter
server.

Example Jupyter Notebooks
----------------------------------

* [basic_jupyter_help_tutorial.ipynb](basic_jupyter_help_tutorial.ipynb) -- A basic tutorial on getting direct info and help of python modules from within a Jupyter notebook.
* [basic_jupyter_latex_tutorial.ipynb](basic_jupyter_latex_tutorial.ipynb) -- A basic tutorial on using Latex syntax inside a Jupyter notebook.
* [basic_jupyter_scipy_tutorial.ipynb](basic_jupyter_scipy_tutorial.ipynb) -- A basic tutorial on using Jupyter to use the scipy modules.
     
