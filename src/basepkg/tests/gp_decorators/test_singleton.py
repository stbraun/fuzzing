# coding=utf-8
"""Test Singleton decorator."""
__author__ = 'sb'

import unittest

from gp_decorators.singleton import singleton


CAROLINE = 'Caroline'
CAROL = 'Carol'


class SingletonDecoratorTest(unittest.TestCase):

    def test_creation(self):
        an_instance = AnotherClass()
        an_instance.name = CAROL
        self.assertEquals(CAROL, an_instance.name)

    def test_uniqueness(self):
        """Check for Singleton property."""
        instance_1 = SomeClass()
        instance_2 = SomeClass()
        self.assertIs(instance_1, instance_2)

    def test_properties(self):
        """Check for Singleton property."""
        instance_1 = SomeClass()
        instance_1.name = CAROL
        self.assertEquals(CAROL, instance_1.name)
        instance_2 = SomeClass()
        self.assertEquals(CAROL, instance_2.name)
        instance_2.name = CAROLINE
        self.assertEquals(CAROLINE, instance_2.name)
        self.assertIs(instance_1, instance_2)


@singleton
class SomeClass(object):
    """Some class for testing."""


@singleton
class AnotherClass(object):
    """Class with properties."""

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
