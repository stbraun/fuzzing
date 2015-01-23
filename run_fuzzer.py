#!/usr/bin/env python3
# coding=utf-8
"""A simple script to make fuzz-testing more convenient."""

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

    :param test_stats: result of test run.
    """
    print('\nTest Results:\n')
    for key in test_stats:
        print('{}'.format(key))
        for status, count in test_stats[key].items():
            print('\t{}: {}'.format(status, count))


def prepare_test_stats(futures):
    """Get stats from futures and merge.

    :param futures: list of futures holding test results.
    :return: dictionary of combined test results.
    """
    combined = None
    for future in futures:
        res = future.result()
        if combined is None:
            combined = res
        else:
            for k in res.keys():
                try:
                    combined[k].update(res[k])
                except KeyError:
                    print('Key missing: combined[{}]'.format(k))
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
    test_stats = prepare_test_stats(futures)
    show_test_stats(test_stats)
    return 0


if __name__ == '__main__':
    sys.exit(main())
