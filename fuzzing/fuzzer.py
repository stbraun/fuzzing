# coding=utf-8
"""Fuzz testing module.

A Toolbox to create fuzzers for random testing of software.

Copyright (c) 2015 Stefan Braun

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
associated documentation files (the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge, publish, distribute,
sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or
substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE
AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import random
import time
import math
from copy import deepcopy
from collections import Counter
import os.path
from tempfile import mkstemp
import subprocess
import logging
import enum


def logger():
    """Provide logger.

    :return: local logger.
    :rtype: Logger
    """
    lg = logging.getLogger('fuzzing.fuzzer')
    return lg


def fuzz_string(seed_str, runs=100, fuzz_factor=50):
    """A random fuzzer for a simulated text viewer application.

    It takes a string as seed and generates <runs> variant of it.

    :param seed_str: the string to use as seed for fuzzing.
    :param runs: number of fuzzed variants to supply.
    :param fuzz_factor: degree of fuzzing = 1 / fuzz_factor.
    :return: list of fuzzed variants of seed_str.
    :rtype: [str]
    """
    buf = bytearray(seed_str, encoding="utf8")
    variants = []
    for _ in range(runs):
        fuzzed = fuzzer(buf, fuzz_factor)
        variants.append(''.join([chr(b) for b in fuzzed]))
    logger().info('Fuzzed strings: {}'.format(variants))
    return variants


def fuzzer(buffer, fuzz_factor=101):
    """Fuzz given buffer.

    Take a buffer of bytes, create a copy, and replace some bytes with random values.
    Number of bytes to modify depends on fuzz_factor.
    This code is taken from Charlie Miller's fuzzer code.

    :param buffer: the data to fuzz.
    :type buffer: byte array
    :param fuzz_factor: degree of fuzzing.
    :type fuzz_factor: int
    :return: fuzzed buffer.
    :rtype: byte array
    """
    buf = deepcopy(buffer)
    num_writes = random.randrange(math.ceil((float(len(buf)) / fuzz_factor))) + 1
    for _ in range(num_writes):
        random_byte = random.randrange(256)
        random_position = random.randrange(len(buf))
        buf[random_position] = random_byte
    return buf


@enum.unique
class Status(enum.Enum):
    """Status values for test runs."""
    FAILED = 0
    SUCCESS = 1


class TestStatCounter(object):
    """Hold a set of test results."""

    def __init__(self, keys):
        """Prepare instance for test setup.

        :param keys: set of keys_.
        :type keys: [str]
        """
        self.keys_ = set(keys)
        self.stats_ = {}
        for key in keys:
            self.stats_[key] = Counter()

    @property
    def keys(self):
        """Retrieve the set of keys.

        :return: set of keys.
        :rtype: set(str)
        """
        return deepcopy(self.keys_)

    def add(self, key, status):
        """Add a new test result to the statistics.

        :param key: key of the test run. Must be in key set!
        :type key: str
        :param status: status of the test run.
        :type status: Status
        """
        assert key in self.keys_, 'ENSURE: key is valid.'
        self.stats_[key][status] += 1

    def cumulated_counts(self):
        """Return sum over all counters.

        :return: The number of test runs; failed and successful.
        """
        return sum([sum(v.values()) for v in self.stats_.values()])

    def cumulated_counts_for_status(self, status):
        """Return sum over all counters for given status.

        :param status: the status to summarize.
        :type status: Status
        :return: number of tests resulting in status.
        """
        return sum([v[status] for v in self.stats_.values()])

    def retrieve_count(self, key, status):
        """Return count of key / status pair.

        :param key: key to retrieve count for.
        :type key: str
        :param status: status to retrieve count for.
        :type status: Status
        :return: count
        """
        assert key in self.keys_, 'ENSURE: key is valid.'
        assert status in Status, 'ENSURE: status is valid.'
        return self.stats_[key][status]

    def __add__(self, other):
        """Merge test statistics.

        Does not modify the statistics, but creates and returns a new one.

        :param other: test statistics to merge with self.
        :type other: TestStatCounter
        :return: the merged statistics.
        :rtype: TestStatCounter
        """
        combined_keys = self.keys_.union(other.keys_)
        tsc = TestStatCounter(combined_keys)
        for key in self.stats_:
            tsc.stats_[key].update(self.stats_[key])
        for key in other.stats_:
            tsc.stats_[key].update(other.stats_[key])
        return tsc

    def __repr__(self):
        """Create printable representation.

        :return: printable statistics.
        :rtype: str
        """
        count_failed = self.cumulated_counts_for_status(Status.FAILED)
        count_succeeded = self.cumulated_counts_for_status(Status.SUCCESS)
        count_all = count_succeeded + count_failed
        info = 'Tests run/succeeded/failed: {} / {} / {}\n'.format(count_all,
                                                                   count_succeeded,
                                                                   count_failed)
        for key in self.keys_:
            info += '{}\n'.format(key)
            for status in Status:
                count = self.retrieve_count(key, status)
                info += '\t{}: {}\n'.format(status.name, count)
        return info


class FuzzExecutor(object):
    """Run fuzz tests on applications."""

    def __init__(self, app_list, file_list):
        """Take apps under test and test data.

        :param app_list: list of applications.
        :param file_list: list of files for testing.
        """
        self.logger = logging.getLogger('fuzzing.fuzzer.FuzzExecutor')
        self.logger.info('Initializing FuzzExecutor ...')
        self.apps, self.args = FuzzExecutor.__parse_app_list(app_list)
        self.file_list = file_list
        self.fuzz_factor = 251
        keys = [os.path.basename(app) for app in self.apps]
        self.stats_ = TestStatCounter(keys)

    def run_test(self, runs):
        """Run tests and build up statistics.

        :param runs: number of tests to run.
        """
        self.logger.info('Start fuzzing ...')
        for _ in range(runs):
            app = random.choice(self.apps)
            data_file = random.choice(self.file_list)
            fuzzed_file = self._fuzz_data_file(data_file)
            self._execute(app, fuzzed_file)
        self.logger.info('Fuzzing completed.')

    @property
    def stats(self):
        """Retrieve statistics of last run.

        :return: statistic counters.
        :rtype: TestStatCounter
        """
        return self.stats_

    def _fuzz_data_file(self, data_file):
        """Generate fuzzed variant of given file.

        :param data_file: path to file to fuzz.
        :type data_file: str
        :return: path to fuzzed file.
        :rtype: str
        """
        buf = bytearray(open(os.path.abspath(data_file), 'rb').read())
        fuzzed = fuzzer(buf, self.fuzz_factor)
        try:
            _, fuzz_output = mkstemp(prefix='fuzzed_')
            open(fuzz_output, 'wb').write(fuzzed)
        finally:
            pass
        return fuzz_output

    def _execute(self, app_, file_):
        """Run app with file as input.

        :param app_: application to run.
        :param file_: file to run app with.
        :return: success True, else False
        :rtype: bool
        """
        app_name = os.path.basename(app_)
        args = [app_]
        args.extend(self.args[app_])
        args.append(file_)
        process = subprocess.Popen(args)

        time.sleep(1)
        status = {True: Status.SUCCESS, False: Status.FAILED}
        crashed = process.poll()
        result = status[crashed is None]
        self.stats_.add(app_name, result)
        if result is Status.SUCCESS:
            # process did not crash, so just terminate it
            process.terminate()

    @staticmethod
    def __parse_app_list(app_list):
        """Parse list of apps for arguments.

        :param app_list: list of apps with optional arguments.
        :return: list of apps and assigned argument dict.
        :rtype: [String], {String: [String]}
        """
        args = {}
        apps = []
        for app_str in app_list:
            parts = app_str.split("&")
            app_path = parts[0].strip()
            apps.append(app_path)
            if len(parts) > 1:
                args[app_path] = [arg.strip() for arg in parts[1].split()]
            else:
                args[app_path] = []
        return apps, args
