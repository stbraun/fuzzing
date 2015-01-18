[![Build Status](https://travis-ci.org/stbraun/fuzzing.svg?branch=develop)](https://travis-ci.org/stbraun/fuzzing) [![Documentation Status](https://readthedocs.org/projects/fuzzing/badge/?version=latest)](https://readthedocs.org/projects/fuzzing/?badge=latest)


Fuzzing - tools for stress testing arbitrary applications.
==========================================================


Stress testing of applications can be done in lots of different ways.
This package provides an easy to use tool to stress test applications which take files
as parameters. Editors, image viewers, and many more classes of apps come to mind.

The stress test is based on a given set of files, binary or text. Those files are taken
randomly and some bytes are modified also randomly ('fuzzed'). Then the application gets
executed with the fuzzed file. Repeating this over and over again stresses the robustness
for defective input data of the application.

Tutorial and API documentation can be found on [ReadTheDocs](https://readthedocs.org/projects/fuzzing/).

Currently provided:
-------------------

  * Random testing of functions.
  * Random testing of applications taking files.
  * Logging configuration.

Installation
------------

The easiest way to install is via ``easy_install`` or ``pip``:

    $ pip install fuzzing



Copyright & License
-------------------

  * Copyright 2015, Stefan Braun
  * License: MIT

