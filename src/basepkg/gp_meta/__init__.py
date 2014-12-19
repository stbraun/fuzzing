# coding=utf-8
"""Meta classes

Copyright 2014, Stefan Braun
Licensed under MIT.
"""

from .singleton import Singleton
import logging

# Symbols available when importing with *.
__all__ = ['Singleton']

# Configure NullHandler to prevent warning in case logging is not configured.
# See https://docs.python.org/2/howto/logging.html#library-config
logging.getLogger('gp_meta').addHandler(logging.NullHandler())

