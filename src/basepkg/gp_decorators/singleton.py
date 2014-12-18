# coding=utf-8
"""A decorator for Singleton classes."""
__author__ = 'sb'

import wrapt

_instances = {}


@wrapt.decorator
def singleton(wrapped, _, args, kwargs):
    """Return the single instance of wrapped.
    :param wrapped: the wrapped class.
    :param _: unused
    :param args: optional arguments for wrapped object.
    :param kwargs: optional arguments for wrapped object.
    """
    global _instances
    if wrapped not in _instances:
        _instances[wrapped] = wrapped(*args, **kwargs)
    return _instances[wrapped]