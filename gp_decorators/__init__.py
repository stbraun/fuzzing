# coding=utf-8
"""Decorators.

Copyright 2014, Stefan Braun
Licensed under MIT.
"""

import logging
from gp_decorators import singleton

# Symbols available when importing with *.
__all__ = ['singleton']

# Configure NullHandler to prevent warning in case logging is not configured.
# See https://docs.python.org/2/howto/logging.html#library-config
logging.getLogger('gp_decorators').addHandler(logging.NullHandler())
