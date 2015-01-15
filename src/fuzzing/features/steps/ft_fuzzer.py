# coding=utf-8
"""Test steps for feature 'fuzzer'."""

from behave import *

from gp_tools.fuzzer import fuzzer, fuzz_string, FuzzExecutor


@given("a byte array of len 10")
def step_impl(context):
    """Prepare a byte array.

    :param context: test context.
    """
    context.buf = bytearray(10)


@when("feeding it into the fuzzer, setting the fuzz_factor to 10")
def step_impl(context):
    """Execute fuzzer.

    :param context: test context.
    """
    context.fuzzed_buf = fuzzer(context.buf, 10)


@then("it will return a buffer with up to two modified bytes.")
def step_impl(context):
    """Check assertions.

    :param context: test context.
    """
    assert len(context.buf) == len(context.fuzzed_buf)
    count = number_of_modified_bytes(context.buf, context.fuzzed_buf)
    assert count < 3
    assert count >= 0


@when("feeding it into the fuzzer, setting the fuzz_factor to {fuzz_factor:d}")
def step_impl(context, fuzz_factor):
    """Execute fuzzer.

    :param fuzz_factor: specified fuzz_factor.
    :param context: test context.
    """
    context.fuzzed_buf = fuzzer(context.buf, fuzz_factor)


@then("it will return a buffer with up to {max_modified:d} modified bytes.")
def step_impl(context, max_modified):
    """Check assertions.

    :param max_modified: maximum expected number of modifications.
    :param context: test context.
    """
    assert len(context.buf) == len(context.fuzzed_buf)
    count = number_of_modified_bytes(context.buf, context.fuzzed_buf)
    assert count >= 0
    assert count <= max_modified


@given("a string as seed.")
def step_impl(context):
    """Provide a string.

    :param context: test context.
    """
    context.seed = context.text


@when("feeding the seed into the fuzzer, providing a count of {count:d}")
def step_impl(context, count):
    """Execute fuzzer.

    :param count: number of string variants to generate.
    :param context: test context.
    """
    fuzz_factor = 11
    context.fuzzed_string_list = fuzz_string(context.seed, count, fuzz_factor)


@then("it will return a list of {len_list:d} fuzzed variants of the seed.")
def step_impl(context, len_list):
    """Check assertions.

    :param len_list: expected number of variants.
    :param context: test context.
    """
    assert len(context.fuzzed_string_list) == len_list
    for fuzzed_string in context.fuzzed_string_list:
        assert len(context.seed) == len(fuzzed_string)
        count = number_of_modified_bytes(context.seed, fuzzed_string)
        assert count >= 0

# ## file fuzzer


@given("a list of file paths")
def step_impl(context):
    """Create file list.

    :param context: test context.
    """
    assert context.table, "ENSURE: table is provided."
    context.file_list = [row['file_path'] for row in context.table.rows]


@given("a list of applications")
def step_impl(context):
    """Create application list.

    :param context: test context.
    """
    assert context.table, "ENSURE: table is provided."
    context.app_list = [row['application'] for row in context.table.rows]


@given("a FuzzExecutor instance created with those lists.")
def step_impl(context):
    """Create application list.

    :param context: test context.
    """
    assert context.app_list and len(context.app_list) > 0, "ENSURE: app list is provided."
    assert context.file_list and len(context.file_list) > 0, "ENSURE: file list is provided."
    context.fuzz_executor = FuzzExecutor(context.app_list, context.file_list)
    assert context.fuzz_executor, "VERIFY: fuzz executor created."


@when("running a test {runs:d} times")
def step_impl(context, runs):
    """Execute multiple runs.

    :param runs: number of test runs to perform.
    :param context: test context.
    """
    executor = context.fuzz_executor
    executor.run_test(runs)
    assert sum(executor.stats.values()) == runs, "VERIFY: stats available."


@then("a randomly chosen application will be called with a randomly chosen file.")
def step_impl(context):
    """Check called apps / files.

    :param context: test context.
    """
    executor = context.fuzz_executor
    pairs = executor.test_pairs
    app_2_files = {}
    for app, file in pairs:
        if app not in app_2_files:
            app_2_files[app] = []
        if file not in app_2_files[app]:
            app_2_files[app].append(file)
    if len(pairs) > 10 and len(context.file_list) > 1:
        multiple_files = False
        for app, files in app_2_files.items():
            multiple_files = context.file_list or len(files) > 0
        assert multiple_files, "VERIFY: at least one app was tested with multiple files."


@then("{runs:d} results are recorded.")
def step_impl(context, runs):
    """Check called apps / files.

    :param runs: expected number of records.
    :param context: test context.
    """
    executor_ = context.fuzz_executor
    assert sum(executor_.stats.values()) == runs, "VERIFY: Number of recorded runs."
    print("\nresults: ", executor_.stats)
    for app, count in executor_.stats.items():
        assert count > 0, "VERIFY: at least one test must have been performed and recorded."


@then("{runs:d} results are recorded and succeeded.")
def step_impl(context, runs):
    """Check called apps / files.

    :param runs: expected number of records.
    :param context: test context.
    """
    executor_ = context.fuzz_executor
    assert sum(executor_.stats.values()) == runs, "VERIFY: Number of recorded runs."
    successful_runs = __get_counts(executor_.stats.items(), 'succeeded')
    assert successful_runs == runs
    for app, count in executor_.stats.items():
        assert count > 0, "VERIFY: at least one test must have been performed and recorded."


@then("{runs:d} results are recorded and failed.")
def step_impl(context, runs):
    """Check called apps / files.

    :param runs: expected number of records.
    :param context: test context.
    """
    executor_ = context.fuzz_executor
    assert sum(executor_.stats.values()) == runs, "VERIFY: Number of recorded runs."
    failed_runs = __get_counts(executor_.stats.items(), 'failed')
    assert failed_runs == runs
    for app, count in executor_.stats.items():
        assert count > 0, "VERIFY: at least one test must have been performed and recorded."

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


def __get_counts(items, status):
    """Get counts for test runs finished with given status.

    :param items: iterable holding (key: count) pairs of test runs.
    :param status: result status. status in {'succeeded', 'failed'}
    :type status: String
    :return: the number of test runs finished with given status.
    """
    return sum([cnt for key, cnt in items if key[1] == status])
