# coding=utf-8
"""Test steps for feature 'singleton'."""

from behave import when, given, then

from gp_decorators.singleton import singleton


@given("two functionally identical classes, one is a singleton.")
def step_impl01(context):
    """Create test classes.
    :param context: test context.
    """
    context.GeneralStore = GeneralStore
    context.SingleStore = SingleStore


@when("creating an instance of the non-singleton class")
def step_impl02(context):
    """Put instance into context for later use.

    :param context: test context.
    """
    context.generalStore = context.GeneralStore()


@when("creating an instance of the singleton class")
def step_impl03(context):
    """Put instance of singleton class into context.

    :param context: test context.
    """
    context.singleStore = context.SingleStore()


@then("the functional behavior is identical.")
def step_impl04(context):
    """Compare behavior of singleton vs. non-singleton.

    :param context: test context.
    """
    single = context.singleStore
    general = context.generalStore
    key = 13
    item = 42
    assert single.request(key) == general.request(key)
    single.add_item(key, item)
    general.add_item(key, item)
    assert single.request(key) == general.request(key)


@given("a singleton class.")
def step_impl05(context):
    """Just put singleton class into context.

    :param context: test context.
    """
    context.SingleStore = SingleStore


@when("creating multiple objects from the class")
def step_impl06(context):
    """Prepare test for singleton property.

    :param context: test context.
    """
    store = context.SingleStore
    context.st_1 = store()
    context.st_2 = store()
    context.st_3 = store()


@then("all will be identical.")
def step_impl07(context):
    """Test for singleton property.

    :param context: test context.
    """
    assert context.st_1 is context.st_2
    assert context.st_2 is context.st_3


@when("modifying the value of an attribute in one of them")
def step_impl08(context):
    """

    :param context: test context.
    """
    context.key = 'the key'
    context.value = 'the value'
    context.st_1.add_item(context.key, context.value)


@then("this modification is visible to all.")
def step_impl09(context):
    """

    :param context: test context.
    """
    assert context.st_1.request(context.key) == context.value
    assert context.st_2.request(context.key) == context.value
    assert context.st_3.request(context.key) == context.value


@then("type() shall return the class.")
def step_impl10(context):
    """

    :param context: test context.
    """
    assert context.SingleStore.__class__ == SingleStore.__class__
    assert issubclass(context.SingleStore, BaseStore)


@then("__module__ shall be the module of the class.")
def step_impl11(context):
    """Test for module.

    :param context: test context.
    """
    assert context.SingleStore.__module__ == BaseStore.__module__


# ###### helpers


class BaseStore(object):
    """Class for test purposes only."""

    def __init__(self):
        self.cache_ = {}

    def add_item(self, k, v):
        """Add an item.
        :param k: key.
        :param v: value.
        """
        self.cache_[k] = v

    def request(self, k):
        """Request an item by key.
        :param k: key.
        """
        if k not in self.cache_:
            return None
        return self.cache_[k]


class GeneralStore(BaseStore):
    """Non-singleton class."""
    pass


# noinspection PyArgumentList
@singleton
class SingleStore(BaseStore):
    """Singleton class."""
    pass
