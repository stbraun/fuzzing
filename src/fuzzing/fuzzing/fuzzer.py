# coding=utf-8
"""Fuzz testing module.

A Toolbox to create fuzzers for random testing of software.
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
        self.stats_ = Counter()
        self.test_pairs_ = []

    def run_test(self, runs):
        """Run tests and build up statistics.

        :param runs: number of tests to run.
        """
        self.logger.info('Start fuzzing ...')
        for _ in range(runs):
            app = random.choice(self.apps)
            data_file = random.choice(self.file_list)
            app_name = os.path.basename(app)
            file_name = os.path.basename(data_file)
            self.test_pairs_.append((app_name, file_name))
            fuzzed_file = self._fuzz_data_file(data_file)
            self._execute(app, fuzzed_file)
        self.logger.info('Fuzzing completed.')

    @property
    def stats(self):
        """Retrieve statistics of last run.

        The stats consist of a Counter with
            * key = (<app-name>, <result>) and
            * value = <number of runs>.

        :return: statistic counters.
        :rtype: Counter
        """
        return self.stats_

    @property
    def test_pairs(self):
        """Retrieve (app, file) pair list of last test run.

        :return: (app, file) pairs of last run.
        :rtype: [(str, str)]
        """
        return self.test_pairs_

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
        crashed = process.poll()
        if crashed:
            self.stats_[(app_name, 'failed')] += 1
        else:
            process.terminate()
            self.stats_[(app_name, 'succeeded')] += 1
        return True

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
