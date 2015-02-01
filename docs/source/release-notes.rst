=============
Release Notes
=============

**Release 0.3.0**

New features:

* Run multiple tests in parallel on multiple processors. Number of processors and processes is configurable.
* Test statistics of the processes are merged and printed.

API changes:

* ``FuzzExecutor.stats`` returns an instance of ``TestStatCounter``, not a simple dict anymore.

You may want to look into ``TestStatCounter`` and ``Status``.
See also ``run_fuzzer.py`` for intended usage.


**Release 0.2.3**

* Data structure for run statistics improved.
* Tests can now be configured using a YAML file.
* Test runner script added for improved user experience ::
    run_fuzzer.py config.yaml

Reading the test runner script may help to get a clearer picture how to use the tool.


**Release 0.2.3a1**

Package structure simplified.


**Release 0.2.2**

Mainly cleanup.

* Test uses pure Python test app. See ``features/resources/testfuzz.py``.


**Release 0.2.1**

* Class ``LoggerFactory``. Logger factory for configuration of the Python logging framework.

* The ``fuzzer`` module uses logging.

* Singleton decorator behaves much nicer since using ``wrapt``.
  See `Graham Dumpleton's talk <https://www.youtube.com/watch?v=W7Rv-km3ZuA&spfreload=10>`_
  on the workings of wrapt.


**Release 0.2.0**

Improved fuzz testing.

* Class ``FuzzExecutor`` makes fuzz testing of applications taking data files easy.


**Release 0.1.0**

First small step.

* Basic functions for fuzz testing.
* Decorator to declare a class as Singleton.
