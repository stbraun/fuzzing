#!/usr/bin/env python3
# coding=utf-8
"""A simple script to make fuzz-testing more convenient."""

import sys
import argparse
import yaml

from fuzzing import FuzzExecutor

APPLICATIONS = 'applications'
SEED_FILES = 'seed_files'
RUNS = 'runs'
DEFAULT_RUNS = 10

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
    if APPLICATIONS not in conf_dict.keys() or SEED_FILES not in conf_dict.keys():
        raise InvalidConfigurationError
    if RUNS not in conf_dict.keys():
        conf_dict[RUNS] = DEFAULT_RUNS
    return


def execute_test(config):
    """Run tests.

    :param config: test configuration.
    :type config: {}
    """
    executor = FuzzExecutor(config[APPLICATIONS], config[SEED_FILES])
    executor.run_test(config[RUNS])
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
    test_stats = execute_test(configuration)
    print("... finished")
    show_test_stats(test_stats)
    return 0


if __name__ == '__main__':
    sys.exit(main())
