# coding=utf-8
"""Provide a meta class implementing the Singleton pattern."""

__author__ = 'sb'


class Singleton(type):
    """Singleton meta class.

    Usage:
    class SomeClass(object, metaclass=Singleton):
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """Guarantee a single instance of each cls."""
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
