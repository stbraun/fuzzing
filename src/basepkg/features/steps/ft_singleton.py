# coding=utf-8
"""Test steps for feature 'singleton'."""

from behave import *

from gp_decorators.singleton import singleton


@given("two functionally identical classes, one is a singleton.")
def step_impl(context):
    """Create test classes."""
    context.GeneralStore = GeneralStore
    context.SingleStore = SingleStore


@when("creating an instance of the non-singleton class")
def step_impl(context):
    context.generalStore = context.GeneralStore()


@when("creating an instance of the singleton class")
def step_impl(context):
    context.singleStore = context.SingleStore()


@then("the functional behavior is identical.")
def step_impl(context):
    """Compare behavior of singleton vs. non-singleton."""
    single = context.singleStore
    general = context.generalStore
    key = 13
    item = 42
    assert single.request(key) == general.request(key)
    single.add_item(key, item)
    general.add_item(key, item)
    assert single.request(key) == general.request(key)


@given("a singleton class.")
def step_impl(context):
    """Just put singleton class into context."""
    context.SingleStore = SingleStore

@when("creating multiple objects from the class")
def step_impl(context):
    Store = context.SingleStore
    context.st_1 = Store()
    context.st_2 = Store()
    context.st_3 = Store()

@then("all will be identical.")
def step_impl(context):
    assert context.st_1 is context.st_2
    assert context.st_2 is context.st_3

@when("modifying the value of an attribute in one of them")
def step_impl(context):
    context.key = 'the key'
    context.value = 'the value'
    context.st_1.add_item(context.key, context.value)

@then("this modification is visible to all.")
def step_impl(context):
    assert context.st_1.request(context.key) == context.value
    assert context.st_2.request(context.key) == context.value
    assert context.st_3.request(context.key) == context.value

# ###### helpers


class BaseStore(object):
    """Class for test purposes only."""

    def __init__(self):
        self.cache_ = {}

    def add_item(self, k, v):
        """Add an item."""
        self.cache_[k] = v

    def request(self, k):
        """Request an item by key."""
        if k not in self.cache_:
            return None
        return self.cache_[k]


class GeneralStore(BaseStore):
    """Non-singleton class."""
    pass


@singleton
class SingleStore(BaseStore):
    """Singleton class."""
    pass
