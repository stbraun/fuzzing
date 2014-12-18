Release Notes
=============


Release 0.2.1
-------------

* Class ``LoggerFactory``. Logger factory for configuration of the Python logging framework.

* Singleton decorator utilizes wrapt behaving much nicer.
See https://www.youtube.com/watch?v=W7Rv-km3ZuA&spfreload=10 for Graham Dumpleton's talk
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
* Meta class for Singletons (deprecated in favor of decorator).
