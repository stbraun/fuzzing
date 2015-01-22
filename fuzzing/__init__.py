# coding=utf-8
"""Tools for development.

Logger.
Random testing tool.

Copyright 2014, Stefan Braun
Licensed under MIT.
"""

from .log import LoggerFactory
from .fuzzer import fuzzer, fuzz_string, FuzzExecutor, TestStatCounter
import logging


# Symbols available when importing with *.
__all__ = ['LoggerFactory', 'fuzzer', 'fuzz_string', 'FuzzExecutor', 'TestStatCounter']


# Configure NullHandler to prevent warning in case logging is not configured.
# See https://docs.python.org/2/howto/logging.html#library-config
logging.getLogger('fuzzing').addHandler(logging.NullHandler())
