Tutorial
========

The following sections will show how to use the classes and functions of the package.


Create Singletons
-----------------

Singleton classes are characterized by the fact that there will be never more than a single instance.
This may be useful for classes handling physical devices or any other stateful objects, e.g. caches,
that need to be handled in a consistent way.

Singletons should be used with care, because they may lead to high coupling if used in many places.
So they may be comfortable first, but become a nightmare later on when extending or maintaining an application.

A singleton class can be created based on a meta class or using a decorator.
Using the decorator is the preferred way. Meta class will likely be deprecated soon.

Creating a singleton class using the singleton decorator is simple: ::

    from gp_decorators.singleton import singleton

    @singleton
    class SomeClass(object):
        """A singleton class."""
        <your code>



Usage of Singleton meta class with Python3: ::

    from gp_meta.singleton import Singleton

    class SomeClass(object, metaclass=Singleton):
        <your code>

For Python2 use the following syntax: ::

    class SomeClass(object):
        __metaclass__ = Singleton
        <your code


.. index:: Random testing

Random testing
--------------

Systematic testing helps us to cover classes of equivalent test cases.
Specifying those test classes largely reduces the effort for testing without sacrificing test coverage.

One drawback of this approach is that we're testing only what we expect to break. This may allow defects
caused by unexpected side effects or unexpected input data to pass the tests ... and show up in production systems.

Random testing is an approach to increase the coverage of the domain of our software's inputs by automatically
running large amounts of tests with randomized input data. This might be totally random 'byte noise',
mostly valid data provided by a carefully crafted generator, or anything in between.

.. index:: ! Charlie Miller

Charlie Miller did some interesting work on fuzz testing. The function fuzzer() is
taken from *Babysitting an Army of Monkeys* (see references below).

**References:**

-  http://fuzzinginfo.files.wordpress.com/2012/05/cmiller-csw-2010.pdf
-  https://cansecwest.com/csw08/csw08-miller.pdf


How to do random testing on your own?
_____________________________________

Fuzz testing can be done on different levels:

- unit (e.g. function, class, module),
- integration (components built from units),
- system (e.g. application).

In each case you need to provide a source for test data, call your SUT, and check the result.
Put this into a loop and start fuzzing.

This is already good for robustness tests. In most cases you also want a kind
of statistics and a documentation of the test cases resulting in an error.

Generating test data
____________________

.. index:: Charlie Miller

In general random testing can be done with any kind of input data (I guess ;-).
The code found in ``gp_tools.fuzzer.fuzzer()`` is working on a binary buffer. It is a copy of
Charlie Miller's code mentioned above.

The binary buffer may contain something
like a pdf, an image, a presentation and so on. It also works fine for normal text, covering
ASCII texts, HTML, XML, JSON and other text based formats.
``gp_tools.fuzzer.fuzz_string()`` is a wrapper simplifying such use cases a bit.

Example of a simple generator:
______________________________

::

    import gp_tools.fuzzer as fuzzer
    seed = "This could be the content of a huge text file."
    number_of_fuzzed_variants_to_generate = 10
    fuzz_factor = 7
    fuzzed_data = fuzzer.fuzz_string(seed, number_of_fuzzed_variants_to_generate, fuzz_factor)
    print(fuzzed_data)

Of course you can also create one fuzzed variant at a time and feed it directly into the SUT.


Calling the SUT with the test data
__________________________________

How to call the SUT depends obviously from its type. A Python function can be called directly with the created
data. It might make sense to enclose the call into a try / except block to catch errors. It is also easy to
check the result value for failure.

Testing software written in other languages works in the same way. You may want to write the fuzz generator in the
target language, or just create the test data with Python and put it into a file for use by the target system.

Applications reading files can be tested creating fuzzed files in the same manner as described above:
Read a valid seed file into a buffer, fuzz it and write it back to a new file. Then run the application
in a separate process for each fuzzed file. In this case it is not that easy to gather useful
information about the success or failure of the run. At least crashes are easily recognized.


The oracle - or: How to evaluate the test result?
_________________________________________________

The function evaluating the result of a test run is called *oracle*. That's fine because the result
is not always clear and understandable.

Running an application in a separate process as described above let us quite easily detect crashes.
If we need more detailed information there is no general way to get at it. One of the most general
information is a crash dump of the SUT.

Detecting issues not leading to a crash depends largely on
the application we are looking at. If it creates some accessible output, like a processed file
or a log file, we may be able to write parsers that enable us to look for failures.


Complete example:
_________________

The following sample code runs 100 tests against the applications listed in ``apps_under_test``.
Test data is generated using a simple fuzzer on a set of files defines in ``file_list``.

After finishing the test runs a statistic is printed.

Note that num_tests should be much bigger for real testing. But it makes sense to start with a small number
to get the test harness working. Then increase this number to a couple of millions or so.

Some of the code found in the ``fuzzer`` module is inlined for easier comprehension.

::

    import math
    import random
    import subprocess
    import time
    import os.path
    from tempfile import mkstemp
    from collections import Counter


    # Files to use as initial input seed.
    file_list = ["./data/pycse.pdf", "./data/PyOPC.pdf", "./data/003_overview.pdf",
                 "./data/Clean-Code-V2.2.pdf", "./data/GraphDatabases.pdf",
                 "./data/Intro_to_Linear_Algebra.pdf", "./data/zipser-1988.pdf",
                 "./data/QR-denkenswert.JPG"]

    # List of applications to test.
    apps_under_test = ["/Applications/Adobe Reader 9/Adobe Reader.app/Contents/MacOS/AdobeReader",
                       "/Applications/PDFpen 6.app/Contents/MacOS/PDFpen 6",
                       "/Applications/Preview.app/Contents/MacOS/Preview",
                       ]


    fuzz_factor = 50  # 250
    num_tests = 100

    # ##### End of configuration #####

    def fuzzer():
        """Fuzzing apps."""
        stat_counter = Counter()
        for cnt in range(num_tests):
            file_choice = random.choice(file_list)
            app = random.choice(apps_under_test)
            app_name = app.split('/')[-1]
            file_name = file_choice.split('/')[-1]

            buf = bytearray(open(os.path.abspath(file_choice), 'rb').read())

            # Charlie Miller's fuzzer code:
            num_writes = random.randrange(math.ceil((float(len(buf)) / fuzz_factor))) + 1

            for _ in range(num_writes):
                r_byte = random.randrange(256)
                rn = random.randrange(len(buf))
                buf[rn] = r_byte
            # end of Charlie Miller's code

            fd, fuzz_output = mkstemp()
            open(fuzz_output, 'wb').write(buf)

            process = subprocess.Popen([app, fuzz_output])

            time.sleep(1)
            crashed = process.poll()
            if crashed:
                logger.error("Process crashed ({} <- {})".format(app, file_choice))
                stat_counter[(app_name, 'failed')] += 1
            else:
                process.terminate()
                stat_counter[(app_name, 'succeeded')] += 1
        return stat_counter

    if __name__ == '__main__':
        stats = fuzzer()
        print(stats)



Using FuzzExecutor
__________________

Fuzz testing applications using files can be used often because it is quite generic. Therefore
it makes sense to encapsulate this functionality and make it easy to apply.

The example above can be written much faster using the class ``FuzzExecutor``: ::

    from gp_tools.fuzzer import FuzzExecutor

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

The property ``FuzzExecutor.stat`` is an instance of ``collections.Counter``. It holds the number
of successful and failed runs for each application.

Another property, ``FuzzExecutor.test_pairs``, provides a list of all test runs in
form of (application, file) tuples.

..  TODO - rewrite this after introducing logging.

**Note:** When running a lot of tests this list might get too big. Then
it is better to remove this feature. In a later release it may be replaced
by logging mechanism.
