# coding=utf-8
"""Test steps for feature 'fuzzer'."""

from behave import *

from gp_tools.fuzzer import fuzzer, fuzz_string


@given("a bytearray of len 10")
def step_impl(context):
    """Prepare a bytearray."""
    context.buf = bytearray(10)


@when("feeding it into the fuzzer, setting the fuzz_factor to 10")
def step_impl(context):
    """Execute fuzzer."""
    context.fuzzed_buf = fuzzer(context.buf, 10)

@then("it will return a buffer with up to two modified bytes.")
def step_impl(context):
    """Check assertions."""
    assert len(context.buf) == len(context.fuzzed_buf)
    count = number_of_modified_bytes(context.buf, context.fuzzed_buf)
    assert count < 3
    assert count > 0


@when("feeding it into the fuzzer, setting the fuzz_factor to 1")
def step_impl(context):
    """Execute fuzzer."""
    context.fuzzed_buf = fuzzer(context.buf, 10)

@then("it will return a buffer with up to 10 modified bytes.")
def step_impl(context):
    """Check assertions."""
    assert len(context.buf) == len(context.fuzzed_buf)
    count = number_of_modified_bytes(context.buf, context.fuzzed_buf)
    assert count > 0


@given("a string as seed.")
def step_impl(context):
    """Provide a string."""
    context.seed = """A test seed for our fuzz tester.
                      Multiple lines are fine."""

@when("feeding the seed into the fuzzer, providing a count of 5")
def step_impl(context):
    """Execute fuzzer."""
    fuzz_factor = 11
    context.fuzzed_string_list = fuzz_string(context.seed, 5, fuzz_factor)

@then("it will return a list of 5 fuzzed variants of the seed.")
def step_impl(context):
    """Check assertions."""
    assert len(context.fuzzed_string_list) == 5
    for fuzzed_string in context.fuzzed_string_list:
        assert len(context.seed) == len(fuzzed_string)
        count = number_of_modified_bytes(context.seed, fuzzed_string)
        assert count > 0


# ##### helpers

def number_of_modified_bytes(buf, fuzzed_buf):
    """Determine the number of differing bytes.

    :param buf: original buffer.
    :param fuzzed_buf: fuzzed buffer.
    :return: number of different bytes.
    :rtype: int
    """
    count = 0
    for idx, b in enumerate(buf):
        if b != fuzzed_buf[idx]:
            count += 1
    return count
