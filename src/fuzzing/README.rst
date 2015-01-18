==================================================================
fuzzing: tools for stress testing arbitrary applications.
==================================================================

.. image:: https://travis-ci.org/stbraun/fuzzing.svg?branch=develop

.. image:: https://readthedocs.org/projects/fuzzing/badge/?version=latest

Stress testing of applications can be done in lots of different ways.
This package provides an easy to use tool to stress test applications which take files
as parameters. Editors, image viewers, and many more classes of apps come to mind.

The stress test is based on a given set of files, binary or text. Those files are taken
randomly and some bytes are modified also randomly (fuzzing). Then the application gets
executed with the fuzzed file. Repeating this over and over again stresses the robustness
for defective input data of the application.

Tutorial and API documentation can be found on ReadTheDocs_.

.. _ReadTheDocs: http://fuzzing.readthedocs.org/.


Currently provided:

  * Random testing of functions.
  * Random testing of applications taking files.
  * Logging configuration.

Installation
------------

The easiest way to install is via ``easy_install`` or ``pip`` ::

    $ pip install fuzzing


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
        for k, v in stats.items():
            print('{} = {}'.format(k, v))




Copyright & License
-------------------

  * Copyright 2015, Stefan Braun
  * License: MIT
