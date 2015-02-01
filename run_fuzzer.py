#!/usr/bin/env python3
# coding=utf-8
"""A simple script to make fuzz-testing more convenient.

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

import sys
import argparse
from concurrent.futures import ProcessPoolExecutor
import yaml

from fuzzing import FuzzExecutor, TestStatCounter


APPLICATIONS = 'applications'
SEED_FILES = 'seed_files'
PROCESSORS = 'processors'
PROCESSES = 'processes'
RUNS = 'runs'
DEFAULT_RUNS = 10
DEFAULT_PROCESSORS = 1
DEFAULT_PROCESSES = 3

help_configuration = """
version: 1
seed_files: ['requirements.txt', 'README.rst']
applications: ['python & features/resources/testfuzz.py -p 0.5']
runs: 15
processors: 3
processes: 8
"""


class InvalidConfigurationError(Exception):
    """Raised if test configuration is invalid."""
    pass


def load_configuration(conf_path):
    """Load and validate test configuration.

    :param conf_path: path to YAML configuration file.
    :return: configuration as dict.
    """
    with open(conf_path) as f:
        conf_dict = yaml.load(f)
    validate_config(conf_dict)
    return conf_dict


def validate_config(conf_dict):
    """Validate configuration.

    :param conf_dict: test configuration.
    :type conf_dict: {}
    :raise InvalidConfigurationError:
    """
    # TASK improve validation
    if APPLICATIONS not in conf_dict.keys() or SEED_FILES not in conf_dict.keys():
        raise InvalidConfigurationError
    if RUNS not in conf_dict.keys():
        conf_dict[RUNS] = DEFAULT_RUNS
    if PROCESSES not in conf_dict.keys():
        conf_dict[PROCESSES] = DEFAULT_PROCESSES
    if PROCESSORS not in conf_dict.keys():
        conf_dict[PROCESSORS] = DEFAULT_PROCESSORS
    return


def execute_test(config):
    """Run tests.

    :param config: test configuration.
    :type config: {}
    """
    import os
    print('Starting process: {}'.format(os.getpid()))
    executor = FuzzExecutor(config[APPLICATIONS], config[SEED_FILES])
    executor.run_test(config[RUNS])
    print('Process {} finishes.'.format(os.getpid()))
    return executor.stats


def show_test_stats(test_stats):
    """Print test statistics.

    :param test_stats: result of test runs.
    :type test_stats: TestStatCounter
    """
    print('\n{}'.format('_' * 50))
    print('Test Results:')
    print('{}'.format('_' * 50))
    print(test_stats),
    print('{}\n'.format('_' * 50))


def combine_test_stats(results):
    """Combine the test results.

    :param results: list of test results.
    :type results: [TestStatCounter]
    :return: combined statistics.
    :rtype: TestStatCounter
    """
    combined = TestStatCounter(set())
    for res in results:
        combined += res
    return combined


def main():
    """Read configuration and execute test runs."""
    parser = argparse.ArgumentParser(description='Stress test applications.')
    parser.add_argument('config_path', help='Path to configuration file.')
    args = parser.parse_args()
    try:
        configuration = load_configuration(args.config_path)
    except InvalidConfigurationError:
        print("\nConfiguration is not valid.")
        print('Example:\n{}'.format(help_configuration))
        return 1
    print("Starting up ...")
    futures = []
    with ProcessPoolExecutor(configuration[PROCESSORS]) as executor:
        for _ in range(configuration[PROCESSES]):
            futures.append(executor.submit(execute_test, configuration))
    print("... finished")
    test_stats = combine_test_stats([f.result() for f in futures])
    show_test_stats(test_stats)
    return 0


if __name__ == '__main__':
    sys.exit(main())
