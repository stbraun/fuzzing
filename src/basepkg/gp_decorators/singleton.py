# coding=utf-8
"""A decorator for Singleton classes."""
__author__ = 'sb'


def singleton(cls):
    """Create a singleton instance of cls.

    :param cls: class to instantiate.
    :return: the single instance of cls.
    """
    _instances = {}

    def get_instance(*args, **kwargs):
        """Return the single instance of cls."""
        if cls not in _instances:
            _instances[cls] = cls(*args, **kwargs)
        return _instances[cls]
    return get_instance