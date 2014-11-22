"""Test Singleton meta class."""

import unittest

from ..meta.singleton import Singleton

CAROLINE = 'Caroline'
CAROL = 'Carol'


class SingletonTest(unittest.TestCase):

    def test_creation(self):
        an_instance = SomeClass()
        an_instance.name = CAROL
        self.assertEquals(CAROL)

    def test_uniqueness(self):
        """Check for Singleton property."""
        instance_1 = SomeClass()
        instance_1.name = CAROL
        instance_2 = SomeClass()
        instance_2.name = CAROLINE
        self.assertEquals(instance_1.name, instance_2.name)


class SomeClass(object):
    """Some class for testing."""
    __metaclass__ = Singleton

    def __init__(self):
        self._name = 'Carl'

    @property
    def name(self):
        """Get name."""
        return self._name

    @name.setter
    def name(self, value):
        """Change name.
        :param value: new name.
        """
        self._name = value
