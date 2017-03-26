python_preamble_directory_relative_module
=========================================

[Parent README](../README.md)

Files:

- [non_module_python_script_using_directory_relative_modules](non_module_python_script_using_directory_relative_modules) -- The preamble wrapper that calls the .py script.
- [non_module_python_script_using_directory_relative_modules.py](non_module_python_script_using_directory_relative_modules.py) -- The Python script.

The demonstrates the following:

- Demonstrate the same things as given
  in [python_preamble_basic](../python_preamble_basic/README.md)
  example.

- Dynamically hack in to `sys.path` the directory for a module, and
  execute a function in that module. This is considered to be a hack
  by some, myself included, but I'm including this approach until I
  can find a better way.

  - See
    https://www.quora.com/What-are-some-good-examples-of-how-to-do-relative-imports-in-python-to-re-use-code-and-packages/answer/Vlad-Calin-1
    for an opinion explaining why this is a hack.

  - See https://github.com/jorgenschaefer/elpy/issues/1109 for a post
    I made to the elpy maintainer to see if there is a smarter way.

  - The rationales for why I currently think I need this type of hack:

    - I'm doing active development so I do not want to install the
      module into some virtualenv while repeatedly reexecuting the
      script. So requiring me to create a setup.py file and keep
      installing it is a non-starter.

    - I need to co-locate modules that are used only by the non-module
      .py file within the same current working directory, or its
      subdirectories.


Usage
=====

Execute it:

    cd into_this_directory
    ./non_module_python_script_using_directory_relative_modules

You should see this output:

    some value

