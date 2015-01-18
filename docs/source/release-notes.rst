=============
Release Notes
=============


Release 0.2.2
-------------

Mainly cleanup.

* Test uses pure Python test app. See ``features/resources/testfuzz.py``.


Release 0.2.1
-------------

* Class ``LoggerFactory``. Logger factory for configuration of the Python logging framework.

* The ``fuzzer`` module uses logging.

* Singleton decorator behaves much nicer since using ``wrapt``.
  See `Graham Dumpleton's talk <https://www.youtube.com/watch?v=W7Rv-km3ZuA&spfreload=10>`_
  on the workings of wrapt.


Release 0.2.0
-------------

Improved fuzz testing.

* Class ``FuzzExecutor`` makes fuzz testing of applications taking data files easy.


Release 0.1.0
-------------

First small step.

* Basic functions for fuzz testing.
* Decorator to declare a class as Singleton.
