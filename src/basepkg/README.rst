==================================================================
basepkg: Some general meta classes.
==================================================================

TODO: Modify the whole file as necessary.

This is a "long description" file for the package that you are creating.
If you submit your package to PyPi, this text will be presented on the `public page <http://pypi.python.org/pypi/python_package_boilerplate>`_ of your package.

Note: This README has to be written using `reStructured Text <http://docutils.sourceforge.net/rst.html>`_, otherwise PyPi won't format it properly.

Installation
------------

The easiest way to install most Python packages is via ``easy_install`` or ``pip``::

    $ easy_install basepkg

Usage
-----

TODO: This is a good place to start with a couple of concrete examples of how the package should be used.

The boilerplate code provides a dummy ``main`` function that prints out the word 'Hello'::

    >> from meta import main
    >> main()
    
When the package is installed via ``easy_install`` or ``pip`` this function will be bound to the ``basepkg`` executable in the Python installation's ``bin`` directory (on Windows - the ``Scripts`` directory).

