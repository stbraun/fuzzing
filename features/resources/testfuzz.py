#!/usr/bin/env python
# coding=utf-8
"""Test app for fuzzer."""

import sys
import argparse
from random import random
import time


def main():
    """Test for fuzzer."""
    description = "Simple app to test our fuzzer."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('in_path', help='The name of a file to read.')
    parser.add_argument('-c', '--crash', help='Crash the app!',
                        action="store_true")
    parser.add_argument('-p', '--probability',
                        help='Crash the app with given probability (0.0-1.0)',
                        type=float,
                        default=0.0)
    args = parser.parse_args()
    if args.crash:
        return 1 / 0
    if random() < args.probability:
        return 2 / 0
    time.sleep(3)
    return 0


if __name__ == '__main__':
    sys.exit(main())
