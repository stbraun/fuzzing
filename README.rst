=========================================================
fuzzing: tools for stress testing arbitrary applications.
=========================================================

.. image:: https://travis-ci.org/stbraun/fuzzing.svg?branch=master

.. image:: https://readthedocs.org/projects/fuzzing/badge/?version=master

Stress testing of applications can be done in lots of different ways.
This package provides an easy to use tool to stress test applications which take files
as parameters. Editors, image viewers, and many more classes of apps come to mind.

The stress test is based on a given set of files, binary or text. Those files are taken
randomly and some bytes are modified also randomly (fuzzing). Then the application gets
executed with the fuzzed file. Repeating this over and over again stresses the robustness
for defective input data of the application.

Tutorial and API documentation can be found on ReadTheDocs_.

.. _ReadTheDocs: http://fuzzing.readthedocs.org/.

What's new?
-----------

Now you can run your tests in multiple processes. Test results are combined and printed.


Installation
------------

The easiest way to install is via ``easy_install`` or ``pip`` ::

    $ pip install fuzzing

There are feature related tests that can be run with ``behave`` and unit tests
runnable with ``pytest`` or ``nosetest``.


Example
-------

::

    from fuzzing.fuzzer import FuzzExecutor

    # Files to use as initial input seed.
    file_list = ["./features/data/t1.pdf", "./features/data/t3.pdf", "./features/data/t2.jpg"]

    # List of applications to test.
    apps_under_test = ["/Applications/Adobe Reader 9/Adobe Reader.app/Contents/MacOS/AdobeReader",
                       "/Applications/PDFpen 6.app/Contents/MacOS/PDFpen 6",
                       "/Applications/Preview.app/Contents/MacOS/Preview",
                       ]

    number_of_runs = 13

    def test():
        fuzz_executor = FuzzExecutor(apps_under_test, file_list)
        fuzz_executor.run_test(number_of_runs)
        return fuzz_executor.stats

    def main():
        stats = test()
        print(stats)


Using pre-built test runner and configuration
---------------------------------------------

For convenience a test runner is provided which takes a test configuration.

Example of a configuration YAML file: ::

    version: 1
    seed_files: ['requirements.txt', 'README.rst']
    applications: ['MyFunnyApp', 'AdobeReader']
    runs: 800
    processors: 4
    processes: 10

Then call the test runner in a terminal session: ::

    $ run_fuzzer.py test.yaml

This will execute the tests as configured and print the test result when done: ::

    $ run_fuzzer.py test.yaml
    Starting up ...
    ... finished

    Test Results:

    MyFunnyApp
        succeeded: 4021
        failed: 95
    AdobeReader
        succeeded: 3883
        failed: 1

Copyright & License
-------------------

  * Copyright 2015, Stefan Braun
  * License: MIT
